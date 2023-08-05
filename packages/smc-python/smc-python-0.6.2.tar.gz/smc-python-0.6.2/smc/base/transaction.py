"""
Transactions allow you to perform create operations that will be tracked and
rolled back in the result of a failure.

A transaction can be specified by either decorating a function with atomic()
or using as a context manager. Each create operation performed within a
transaction will be tracked on the users session and rolled back in the event
of a failure.

Currently any failure within the transaction context will trigger a rollback,
however only elements created in the transaction will be rolled back. It is
not possible to roll back deleted elements or elements that were updated or
modified. 

Example of wrapping a function with transaction::

    @transaction.atomic
    def mytasks():
        Host.update_or_create(name='host3', address='1.1.1.1')
        for name in range(1, 4):
            Host.create(name='host%s' % name, address='1.1.1.1')
            
Example of using transactions as a context manager::

    with transaction.atomic():
        Host.update_or_create(name='host3', address='1.1.1.1')
        for name in range(1, 4):
            Host.create(name='host%s' % name, address='1.1.1.1')
            
Transactions can also consist of nested transactions. This represents a
`savepoint` where you want to ensure the changes made are committed and
not rolled back in the event of an error. Think of a savepoint as a partial
transaction.

For example, the following function is wrapped in a transaction and also
includes a nested transaction. The first operation is treated as a `savepoint`
once the inner nested transaction executes. Meaning the creation of host3 will
not be rolled back even if there is a failure within the inner nested
transaction::

    @transaction.atomic
    def mytasks():
        Host.update_or_create(name='host3', address='1.1.1.1')
        
        with transaction.atomic(): # <--- inner nested transaction
            for name in range(1, 4):
                Host.create(name='host%s' % name, address='1.1.1.1')

.. warning:: It is not recommended to catch exceptions stemming from SMCException
    within the transaction. The context manager is expecting exceptions in order
    to trigger the rollback functionality.
"""
import functools
from smc.api.common import _get_session
from smc.api.exceptions import DeleteElementFailed, SMCConnectionError,\
    SMCException


class TransactionError(SMCException):
    def __init__(self, original_exception, message, success, errors):
        message = '%s: %s ' % (original_exception, message)
        if not success and not errors:
            message += 'No changes to rollback.'
        elif success and not errors:
            message += 'Successfully rolled back elements: %s' % success
        elif errors:
            message += 'Errors occurred deleting elements on rollback %s' % errors
        super(TransactionError, self).__init__('%s: %s' % (original_exception, message))
        self.success = success
        self.errors = errors


def atomic(using=None):
    if callable(using):
        return Atomic(_get_session())(using)
    else:
        return Atomic(_get_session(using))


class ContextDecorator(object):
    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwds):
            with self:
                return f(*args, **kwds)
        return decorated


class Atomic(ContextDecorator):
    """
    This is a re-entrant context manager that can also be used as a function
    decorator. Use this when you want to wrap SMC based operations and attempt
    a rollback operation if one of the operations fail.
    This will pertain only to `create` operations performed, so anything
    that calls ElementCreator will be considered as a transaction.

    This is considered a private API.
    """
    def __init__(self, session):
        self._session = session
        self._savepoint = False
    
    def rollback(self):
        """
        Rollback forces any transactions to be deleted in reverse order
        that they were added. Any failures to delete a particular element
        will also be tracked.
        
        This could be useful if you were to catch a specific error type
        within the context manager client code and wanted to execute the
        rollback manually.
        
        """
        rollback_success, rollback_failed = [], []
        for transaction in reversed(self._session.transactions):
            try:
                transaction.delete()
                raise DeleteElementFailed('Big bad error')
                rollback_success.append(transaction)
            except DeleteElementFailed as e:
                rollback_failed.append({'reason': str(e), 'element': transaction})
        return rollback_success, rollback_failed
    
    def savepoint(self):
        """
        Calling savepoint clears the existing queued transactions. A
        savepoint is considered a spot within the context manager where
        modifications should be permanently saved and removed from the
        rollback process should an operation fail after the savepoint is
        called.
        Usage::
        
            with transaction.atomic() as taction:
                Host.update_or_create(name='foo', address='1.1.1.1')
                transaction.savepoint()
                
                .... do more things ....
        
        :return: None
        """
        self._session.transactions[:] = []
        
    def __enter__(self):
        print("Enter: %s" % self._session.in_atomic_block)
        if not self._session.in_atomic_block:
            self._session.in_atomic_block = True
        else:
            print("We are already in an atomic block, setting savepoint, clearing transactions: %s" % (self._session.transactions))
            self._savepoint = True
            self._session.transactions = []
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Called exit, is savepoint: %s, transactions: %s, exc_type: %s" % (self._savepoint, self._session.in_atomic_block, exc_type))
        try:
            if exc_type is not None:

                print("In else, exception occurred: %s, transactions :%s" % (exc_type, self._session.transactions))
                if exc_type in (SMCConnectionError,):
                    return
                
                # Rollback only once we've exited savepoints
                if not self._savepoint:
                    rollback_success, rollback_failed = self.rollback()
        
                    raise TransactionError(exc_type, exc_value, rollback_success, rollback_failed)
                
                print("raise: %s raiser :%s" % (exc_type, exc_value))

        finally:
            print("Called finally..")
            if not self._savepoint:
                # Outer context manager, reset state on session
                self._session.in_atomic_block = False
                self._session.transactions = []
            
            else:
                # Nested context manager within a savepoint, identify ourself
                print("We are in a savepoint, reset upon exit")
                self._savepoint = True

            print("Session vars: %s" % vars(self._session))
            
    
    
"""
Name cache is used on the engine as a mechanism to load mappings into
the kernel for filtering
This is used by multiple mechanisms such as user mappings, dns to IP
mappings and security group (NSX) mappings.
"""
import json


class NameCache(object):
    """
    Name Cache is the engine specific configuration that loads the security
    group and corresponding IP addresses into the kernel for policy control.
    For NSX, any time a policy security group is modified, an NSX action is
    POST'd to the NSX Proxy and we need to process those (possible) changes.
    
    The data structure for the name cache is json and is in the format::
    
        {
           "type":"sec_group",
           "payload":[
              {
                 "action":"update",
                 "name":"foo",
                 "address":"1.1.1.1",
                 "timeout":"never", # int (seconds)
                 "ve_id":1 (optional)
              },
              {
                 "action":"remove", # Remove entry 1.1.1.1 for mygroup on ve_id 1
                 "name":"mygroup",
                 "address":"1.1.1.1",
                 "ve_id":1
              },
              {
                  "action": "remove", # Remove all entries for mygroup from ve_id 1
                  "name": "mygroup",
                  "ve_id": 1
              },
              {
                  "action": "purge", # Purge all from ve_id 1
                  "ve_id": 1
              },
              {
                  "action": "purge", # purge all from engine
              }
           ]
        }
        
    This can be sent over the SMC API or loaded directly over SSH by::
    
        /usr/lib/stonegate/bin/test-name-cache-sockopt --json <file>
    """
    _keys = ('action', 'address', 'name', 'timeout', 've_id')
    
    def __init__(self):
        self.payload = []
    
    def _strip_none(self, kwargs):
        for arg in list(kwargs.keys()):
            if kwargs.get(arg) is None:
                kwargs.pop(arg)
    
    def purge(self, **kwargs):
        kwargs.update(action='purge')
        self._strip_none(kwargs)
        self.payload.append(kwargs)
    
    def update(self, **kwargs):
        kwargs.update(action='update')
        self.payload.append(kwargs)
        
    def remove(self, **kwargs):
        kwargs.update(action='remove')
        self._strip_none(kwargs)
        self.payload.append(kwargs)
    
    def fetch(self, **kwargs):
        kwargs.update(action='fetch')
        self._strip_none(kwargs)
        self.payload.append(kwargs)
        
    def as_dict(self):
        return {'type': self.type, 'payload': self.payload}

    def serialize(self):
        return json.dumps(self.as_dict())


class SecGroup(NameCache):
    type = 'sec_group'
    
    def purge(self, ve_id=None):
        """
        Purge all entries from the engine. If ve_id is specified,
        only purge entries for that virtual engine (applies only
        to master engines).
        
        :param int ve_id: virtual engine id, `vfw_id` in virtual resource
        """
        super(SecGroup, self).purge(ve_id=ve_id)
    
    def update(self, name, address, ve_id, timeout='never'):
        """
        Update entries on engine.
        
        :param str name: name of entry
        :param str address: address for entry
        :param int ve_id: virtual engine id, `vfw_id` in virtual resource
        """
        super(SecGroup, self).update(name=name, address=address,
            ve_id=ve_id, timeout=timeout)
    
    def remove(self, name, ve_id=None, address='any'):
        """
        Remove the following entry from the engine. The ve_id can optionally
        specify the ve_id for which to remove, otherwise remove from which
        ever ve is using the group (two VE's can not use the same group).
        
        Remove securitygroup, regardless of VE::
        
            secgroup.remove('securitygroup-18')
        
        Remove group from specified virtual engine::
            
            secgroup.remove('securitygroup-18', ve_id=1)
            
        Remove using most specific match:: 
        
            secgroup.remove('foo', address='3.3.3.3', ve_id=1)
        
        :param str name: name of entry
        :param str address: address for entry to remove, 'any' for all
        :param int ve_id: virtual engine id, `vfw_id` in virtual resource
        """
        super(SecGroup, self).remove(name=name, address=address,
            ve_id=ve_id)
    
    def fetch(self, name):
        """
        Fetch entries from the engine using name of group as mechanism to
        find the entry.
        ::
        
            secgroup.fetch(name='securitygroup-18')
            
        Returns::
        
            {
               "type": "sec_group",
               "result", [
                     { "name" : "securitygroup-18",
                       "address" : "172.18.1.21",
                       "ve_id" : 1
                     },
                     { "name" : "securitygroup-18",
                       "address" : "fe80::e982:d941:5b95:ba2c",
                       "ve_id" : 1
                     }
                ]
            }
        
        :param str name: name of entry
        :param int ve_id: virtual engine id, `vfw_id` in virtual resource
        """
        super(SecGroup, self).fetch(name=name)

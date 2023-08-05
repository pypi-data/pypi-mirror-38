# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2016

@author: davidlepage
'''
import logging
#from smc import session
from smc.core.engine import Engine, VirtualResource
from smc.elements.servers import LogServer
from smc.base.collection import Search
from smc.core.sub_interfaces import ClusterVirtualInterface
from smc.core.interfaces import ClusterPhysicalInterface, TunnelInterface, Layer3PhysicalInterface

from smc.base.util import element_resolver, datetime_from_ms
from smc.core.engines import Layer3Firewall, MasterEngine
from smc.api.exceptions import ActionCommandFailed, ResourceNotFound,\
    SMCException, CreateElementFailed, DeleteElementFailed, ElementNotFound
from smc.routing.bgp import AutonomousSystem, BGPPeering
from smc.base.transaction import TransactionError
from smc.core.engine_vss import VSSContainer, SecurityGroup,\
    VSSContainerNode, VSSContext
from smc.base.model import prepared_request, SubElement, ElementCache,\
    ElementRef
from smc.elements.user import AdminUser, ApiClient
from smc.administration.tasks import TaskProgress, TaskHistory
from smc.administration.access_rights import AccessControlList
from smc.elements.situations import InspectionSituation, SituationContextGroup,\
    InspectionSituationContext, \
    SituationParameterValue, CorrelationSituation, CorrelationSituationContext
from smc.routing.prefix_list import IPPrefixList
from smc.elements.other import Category, SituationTag
from smc.routing.route_map import RouteMap
from smc.elements.helpers import zone_helper
from smc.vpn.route import TunnelEndpoint, RouteVPN
from smc.core.node import ApplianceStatus
from smc.vpn.elements import ExternalGateway
from smc.elements.service import ICMPService, TCPService
from smc.elements.network import AddressRange
from smc.elements.group import ICMPServiceGroup
from smc.core.waiters import NodeStatusWaiter


logger = logging.getLogger(__name__)

import json

def patch(url, data, etag, **kwargs):
    headers={'Accept': 'application/json-patch+json',
             'Content-Type': 'application/json',
             'If-Match': etag}
    headers.update(kwargs)
    r = session.session.patch(url, data=json.dumps(data), headers=headers)

    print(vars(r))
    print(vars(r.request))

def get_options_for_link(link):
    r = session.session.options(link)  # @UndefinedVariable
    headers = r.headers['allow']
    allowed = []
    if headers:
        for header in headers.split(','):
            if header.replace(' ', '') != 'OPTIONS':
                allowed.append(header)
    return allowed

def head_request(link):
    r = session.session.head(link)  # @UndefinedVariable
    print(vars(r))


if __name__ == '__main__':
    import sys
    import time
    from pprint import pprint
    start_time = time.time()
    
    
    #from requests_toolbelt import SSLAdapter
    #import requests
    #import ssl
    
    #session.set_file_logger(log_level=10, path='/Users/davidlepage/Downloads/smc-test.log')
    #session.set_stream_logger(log_level=logging.DEBUG)
    
    #logging.getLogger()
    #logging.basicConfig(
    #    level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s')
    
    from smc import session, set_stream_logger
    set_stream_logger()
    #set_stream_logger(log_level=logging.DEBUG, logger_name='urllib3')
    
    #session.login(url='http://172.18.1.26:8082', api_key='kKphtsbQKjjfHR7amodA0001')
    
    #session.login(url='https://172.18.1.151:8082', api_key='xJRo27kGja4JmPek9l3Nyxm4',
    #              verify=False, beta=True, timeout=45, retry_on_busy=True)
    
    #xJRo27kGja4JmPek9l3Nyxm4
    
    
    
#     a = ApiClient('smcpython')
#     a.change_password('xJRo27kGja4JmPek9l3Nyxm4')
    
    #session.login(url='http://172.18.1.150:8082', api_key='EiGpKD4QxlLJ25dbBEp20001', timeout=30,
    #              verify=False, beta=True)
    
    session.login(url='https://172.18.1.151:8082', login='myadmin2', pwd='1970keegan', beta=True, verify=False)
    
    #2018-11-02 09:48:35,156 [DEBUG] smc.api.web.debug Thread-129: Request method: GET
    #2018-11-02 09:48:35,156 [DEBUG] smc.api.web.debug Thread-129: Request URL: https://172.18.1.151:8082/6.5/elements?filter=servicebar&exact_match=True&filter_context=vss_container
    data = {u'address': u'1.1.1.5',
              u'key': 487,
              u'link': [{u'href': u'https://172.18.1.151:8082/6.5/elements/host/487',
                         u'rel': u'self',
                         u'type': u'host'},
                        {u'href': u'https://172.18.1.151:8082/6.5/elements/host/487/export',
                         u'rel': u'export'},
                        {u'href': u'https://172.18.1.151:8082/6.5/elements/host/487/history',
                         u'rel': u'history'},
                        {u'href': u'https://172.18.1.151:8082/6.5/elements/host/487/search_category_tags_from_element',
                         u'rel': u'search_category_tags_from_element'},
                        {u'href': u'https://172.18.1.151:8082/6.5/elements/host/487/duplicate',
                         u'rel': u'duplicate'}],
              u'name': u'foohost',
              u'read_only': False,
              u'secondary': [],
              u'system': False}
    
    ETag = 'NDg3MzExMTU0MTI3NTYxMDI0MA=='
    

    #https://172.18.1.151:8082/6.5/elements/host/487
    
    session.session.cookies.set('JSESSIONID', '0C1A04DD76A8B407896070F2A8256379', domain='172.18.1.151')
    
    from smc.elements.network import Host
    Host('foohost').delete()
    
#     import requests
    
#     delete = session.session.delete('https://172.18.1.151:8082/6.5/elements/host/487',
#                              verify=False)
#     
#     print("Delete: %s" % delete)
#     print(vars(delete))
    
    
#     result = requests.post(
#         'https://172.18.1.151:8082/elements/host',
#         data={'name': 'foohost2', 'address': '12.12.12.12'},
#         cookies={'JSESSIONID': '11111111111111111111111111111111'},
#         verify=False)
#     
#     print("Post: %s" % result)
#     print(vars(result))
#     
#     result = requests.put(
#         'https://172.18.1.151:8082/elements/host',
#         data=data, cookies={'JSESSIONID': '0C1A04DD76A8B407896070F2A8256379'},
#         verify=False)
#     
#     
#     print("PUT: %s" % result)
#     print(vars(result))
   
    
    
    sys.exit(1)
    #engine = Engine('engine1')
    #interface = engine.routing.get(1020)
    #pprint(vars(interface.data))
    
#     peering = BGPPeering.get_or_create(name='MyPeering')
#     ext_gw = ExternalGateway.get_or_create(name='MyexternalGW')
#     
#     engine.tunnel_interface.add_layer3_interface(
#         interface_id=1020, address='120.120.120.1', network_value='120.120.120.0/24')
#     
#     routing = engine.routing.get(1020)
#     routing.add_bgp_peering(peering, ext_gw)
    
        
    #TODO: VALIDATE THESE NEW STATUS FIELDS!
    # for example, status, monitoring_status, engine_node_status
    #v6.5
    #2018-10-17 14:56:00,534 - smc.api.web - [DEBUG] - {"configuration_status":"Initial","engine_node_status":"Not Monitored","monitoring_state":"NO_STATUS","monitoring_status":"NOT_MONITORED","name":"engine1 node 1","platform":"N/A","version":"unknown"}
    #2018-10-17 15:02:10,943 - smc.api.web - [DEBUG] - {"configuration_status":"Installed","dyn_up":"1109","engine_node_status":"Online","installed_policy":"Layer 3 Router Policy","monitoring_state":"READY","monitoring_status":"OK","name":"ve-1 node 1","platform":"x86-64-small","version":"version 6.4.2 #20106"}
    #v6.4.3
    #2018-10-17 15:06:15,601 - smc.api.web - [DEBUG] - {"configuration_status":"Initial","name":"engine1 node 1","platform":"N/A","state":"NO_STATUS","status":"Not Monitored","version":"unknown"}

    
    

#     interface0 = engine.interface.get('1.1')
#     interface0.update(
#         zone_ref=zone_helper('Zone Secondary-3 Students'),
#         dhcp_server_on_interface={
#             'default_gateway': '11.11.11.210',
#             'default_lease_time': 7200,
#             'dhcp_address_range': '11.11.11.101-11.11.11.105',
#             'dhcp_range_per_node': [],
#             'primary_dns_server': u'8.8.8.9'})

    
#     interface0 = engine.interface.get(0)
#     interface0.update(
#         dhcp_server_on_interface={
#             'default_gateway': '1.1.1.200',
#             'default_lease_time': 7200,
#             'dhcp_range_ref': AddressRange('foorange').href,
#             'dhcp_range_per_node': [],
#             'domain_name_search_list': 'foo.com',
#             'primary_dns_server': u'8.8.8.9',
#             'primary_wins_server': u'1.1.1.10',
#             'secondary_dns_server': u'8.8.8.8',
#             'secondary_wins_server': u'1.1.1.111'})
    
#         dhcp_server_on_interface={
#             'default_gateway': '1.1.1.200',
#             'default_lease_time': 7200,
#             'dhcp_address_range': '1.1.1.100-1.1.1.105',
#             'primary_dns_server': '8.8.8.9'})
    
    
    #pprint(vars(engine.data))
    
    
    #print(vpn.remote_endpoint.remote_address)
    
    sys.exit(1)
    #container = VSSContainer('foobarservice')
    #pprint(vars(container.data))
    
    '''
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/situation_tag', rel=u'situation_tag', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/tls_match_situation', rel=u'tls_match_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/ei_application_situation', rel=u'ei_application_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/url_list_situation', rel=u'url_list_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/inspection_situation', rel=u'inspection_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/application_situation', rel=u'application_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/situation_context_group', rel=u'situation_context_group', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/correlation_situation', rel=u'correlation_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/url_situation_context', rel=u'url_situation_context', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/tls_match_situation_context', rel=u'tls_match_situation_context', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/inspection_situation_context', rel=u'inspection_situation_context', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/situation_group_tag', rel=u'situation_group_tag', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/eca_operating_system_situation', rel=u'eca_operating_system_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/application_situation_context', rel=u'application_situation_context', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/url_situation', rel=u'url_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/sub_application_situation', rel=u'sub_application_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/sub_tls_match_situation', rel=u'sub_tls_match_situation', method=None)
    EntryPoint(href=u'https://172.18.1.151:8082/6.5/elements/correlation_situation_context', rel=u'correlation_situation_context', method=None)
    '''
    
    
    def situations_by_severity(level):
        return [situation
            for situation in InspectionSituation.objects.all()
            if situation.severity == level]
            
#     for x in Search.objects.entry_point('situation_tag'):
#         pprint(vars(x.data))
#         
    situation = InspectionSituation('mysituation')
    #print(situation.categories)
    #pprint(vars(situation.data))
    
    
    
    
    
    
    #for x in Search.objects.entry_point('situation_tag'):
    #    if x.name == 'Botnet':
    #        pprint(vars(x.data))
    #        print(x.categories)
        
    #print(prepared_request(href='https://172.18.1.151:8082/6.5/elements/situation_tag/3426/search_elements_from_category_tag').read().json)
    #sys.exit(1)
    
    
#     context = InspectionSituationContext('Text File Stream')
#     for parameter in context.situation_parameters:
#         print(parameter)
#         pprint(vars(parameter.data))
    
#     situation = InspectionSituation('File-Text_ActiveX-WScript-Shell-Call')
#     #situation = InspectionSituation('FooSituation')
#     context = situation.situation_context
#     print(context)
#     pprint(vars(context.data))
#     
#     print('-----------------------------')
#     pprint(vars(situation.data))
#     for value in situation.parameter_values:
#         print(value)
#         #print(value.situation_parameter)
#         pprint(vars(value.data))
#     
#     print("Parameter Ref vvvvvvvvvvvvvvvvvvvvvv")    
#     pprint(prepared_request(href='https://172.18.1.151:8082/6.5/elements/inspection_situation_context/353/situation_parameter/90077901').read().json)

#     pprint(vars(situation.data))
#     print(situation.categories)
#     for value in situation.parameter_values:
#         pprint(vars(value.data))
#         print(r'{}'.format(value.data.get('reg_exp')))
#         
#         try:
#             print(json.dumps(value.data.get('reg_exp')))
#         except ValueError as e:
#             print('Invalid json specified: %s' % str(e))
    
        
    
    #regexp = '(?x)\n.*ActiveXObject \\x28 \\x22 WScript\\.Shell(?[s_file_text_script -> sid()])\n'
    regexp = "(?x)\n.*2b62aa-ee0a-4a95-91ae-b064fdb471fcUopnumL:0x0001(?[skip(4),\nparse_le(32)==0x00002711->(\nskip(8),\nregex([^x00]*bwmakdir\\.exe(\\x20)+[\\x30-\\x39] (?[\nregex( [\\x30-\\x39]*(\\x20)+[^\\x20]{65,}(?[sid(),cancel]) ),\nregex( [\\x30-\\x39]*(\\x20)+[^\\x20]{1,64}(\\x20)+[\\x01-\\xff]{257,}(?[sid(),cancel]))\n])))\n])\n"

    #print(json.dumps(regexp))
    #regular_expression = SituationParameterValue.create_regular_expression(
    #    inspection_context=InspectionSituationContext('Text File Stream'),
    #    regexp='(?x)\n.*ActiveXObject \\x28 \\x22 WScript\\.Shell123a(?[s_file_text_script -> sid()])\n')
    
#     foo = InspectionSituation.create(
#         name='customsituation', comment='my test comment',
#         description='Some description for this situation',
#         situation_context=InspectionSituationContext('Text File Stream'),
#         severity='high')
#     
#     #foo = InspectionSituation('customsituation')
#     foo.create_regular_expression(regexp)
    
    test = r"""(?x)
.*2b62aa-ee0a-4a95-91ae-b064fdb471fcUopnumL:0x0001(?[
    skip(4),
    parse_le(32)==0x00002711->(
        skip(8),
        regex([^x00]*bwmakdir\.exe(\x20)+[\x30-\x39] (?[
            regex( [\x30-\x39]*(\x20)+[^\x20]{65,}(?[sid(),cancel]) ),
            regex( [\x30-\x39]*(\x20)+[^\x20]{1,64}(\x20)+[\x01-\xff]{257,}(?[sid(),cancel]) )
            ]) )
        )
])"""
    print(json.dumps(repr(test)))
    
    #test2 = r""".*\x02\x49\x64\x08\x50\x61\x72\x65\x6E\x74\x49\x64\x04\x4E\x61\x6D\x65?(?[CRC(300)==3964681330->sid()])"""
    
    
    
    #print(test2)
    
    #print('dump hex: %s' % json.dumps(repr(test2)))
    
    
    foo = InspectionSituation.create(
        name='customsituation2', comment='my test comment',
        description='Some description for this situation',
        situation_context=InspectionSituationContext('Text File Stream'),
        situation_type=SituationTag('Attacks'),
        severity='high')
    
    #foo.create_regular_expression(repr(test2))
    foo.create_regular_expression(test)
    
    sys.exit(1)
#     
#     
#     print(foo)
    
#     foo = InspectionSituation('mysituation')
#     print("Regexp: %s" % foo.create_regular_expression(regexp))
#     pprint(vars(foo.data))
#     print(foo.situation_context)
#     for param in foo.situation_context.situation_parameters:
#         print(param, vars(param))
#         pprint(vars(param.data))
#        
#     print("------------------------------------------")
#     for value in foo.parameter_values:
#         print(value, vars(value))
#         pprint(vars(value.data))
        
#         
#     #https://172.18.1.151:8082/6.5/elements/inspection_situation_context/353/situation_parameter/90077901
# #         
#     print(foo.add_parameter_value(regular_expression))
    
    #print(get_options_for_link('https://172.18.1.151:8082/6.5/elements/inspection_situation/1073741831/reg_exp_situation_parameter_value/283691'))
    
#     situation = InspectionSituation('FooSituation')
#     print(situation.situation_context)
#     pprint(vars(situation.data))
#     for p in situation.parameter_values:
#         print(p)
    
    #print(get_options_for_link('https://172.18.1.151:8082/6.5/elements/inspection_situation/1073741825/reg_exp_situation_parameter_value'))
    '''
    regex_situation_paramter:
    
    {u'dfas': [u'https://172.18.1.151:8082/6.5/elements/internal_file/410',
               u'https://172.18.1.151:8082/6.5/elements/internal_file/440',
               u'https://172.18.1.151:8082/6.5/elements/internal_file/146'],
     u'key': 139458,
     u'link': [{u'href': u'https://172.18.1.151:8082/6.5/elements/inspection_situation/523746/reg_exp_situation_parameter_value/139458',
                u'rel': u'self',
                u'type': u'reg_exp_situation_parameter_value'}],
     u'name': u'Regular Expression',
     u'order': 0,
     u'parameter_ref': u'https://172.18.1.151:8082/6.5/elements/inspection_situation_context/353/situation_parameter/90077901',
     u'reg_exp': u'(?x)\n.*ActiveXObject \\x28 \\x22 WScript\\.Shell(?[s_file_text_script -> sid()])\n'}
    
    integer_siuation_parameter:
    {u'key': 283673,
     u'link': [{u'href': u'https://172.18.1.151:8082/6.5/elements/inspection_situation/1073741825/integer_situation_parameter_value/283673',
                u'rel': u'self',
                u'type': u'integer_situation_parameter_value'}],
     u'name': u'Maximum unreplied ICMP Timestamp Requests',
     u'order': 3,
     u'parameter_ref': u'https://172.18.1.151:8082/6.5/elements/inspection_situation_context/499/situation_parameter/90015419',
     u'value': 65535}
    '''
#     pprint(vars(context.data))
#     for situation_parameter in context.situation_parameters:
#         print(situation_parameter)
#         pprint(vars(situation_parameter.data))
#     
#     context = InspectionSituation.objects.filter('testfile').first()
#     print("c: %s" % context)
#     pprint(vars(context.data))
#     print(context.situation_context)
#     pprint(prepared_request(href='https://172.18.1.151:8082/6.5/elements/inspection_situation/1073741825/reg_exp_situation_parameter_value/283038').read().json)
#     #print(list(SituationContextGroup.objects.filter('File Type Inspection')))
      
# 
#     i = InspectionSituation('testfile')
#     situation_context = i.situation_context
#     print("Situation_context: %s" % situation_context)
#     pprint(vars(situation_context.data))
#     
#     print("................. Situation .............................")
#     pprint(vars(i.data))
#     for value in i.data.get('parameter_values'):
#         print("Param value: %s" % value)
#         pprint(prepared_request(href=value).read().json)
#         
#     #pprint(prepared_request(href='https://172.18.1.151:8082/6.5/elements/inspection_situation_context/512/situation_parameter/90077901').read().json)    
#     
#     print("Situation context -----------------")
#     
#     # This is the context for the inspection situation vvvvvvvvvv (Text File Stream)
#     pprint(prepared_request(href='https://172.18.1.151:8082/6.5/elements/inspection_situation_context/512').read().json)
#     
#     vss = VSSContainer('srv')
#     
#         
#     sys.exit(1)
    
    
    username = 'nsxadmin'
    password = 'password'
    
    def ssh_command_string(address, as_json=None, as_string=None, bg_run=False):
        """
        Build the command string based on whether this is a direct edit of
        the name cache or using engine version 6.4.3 as a json file.
        This is a workaround until SMC API supports sending this data.
        
        :param str address: IP to build the command,i.e. ssh nsxadmin@foo
        :param dict as_json: valid dict to be dumped to json
        :param list as_string: string list of commands for ngfw <=6.4.3
        """
        ssh_part = 'ssh %s@%s' % (username, address)
        
        stonegate_bin = '/usr/lib/stonegate/bin/test-name-cache-sockopt'
    
        options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'                                                                         
    
        if bg_run:                                                                                                                                                         
            options += ' -f'                                                                                
        
        command = ''
        
        if as_json:
            dict_to_json = json.dumps(as_json)
            dict_escaped = dict_to_json.replace('"', r'\"')  # raw string used here
            #command = "%s %s echo '%s' > /tmp/t.json;%s --json /tmp/t.json;rm /tmp/t.json" % (
            command = "%s %s echo '%s' > /tmp/t.json;%s --json /tmp/t.json" % (
                ssh_part, options, dict_escaped, stonegate_bin)
        
        elif as_string:
            command = '%s %s "%s"' % (ssh_part, options, as_string)  
    
        return command
            
    import tempfile
    import pexpect    # @UnresolvedImport
        
    def run_ssh_command(command_string, timeout=10, restart_dpa=False):
        """
        Run the following SSH command string. The string should be pre-compiled
        and be compatible with python pexpect module.
        
        :param str command_string: command string to launch on FW
        :param int timeout: timeout for pexpect
        :param bool restart_dpa: should DPA be restarted after command is run
        :raises Exception: exception caught from pexpect call
        :return: string output of stdout on success
        """
        fname = tempfile.mktemp()                                                                                                                                                  
        fout = open(fname, 'w')         
        
        logger.debug('SSH command executing: %s', command_string)
        child = pexpect.spawn(command_string, timeout=timeout)                                                                                                                            
        child.expect(['Password: '])                                                                                                                                                                                                                                                                                               
        child.sendline(password)
        if restart_dpa:
            child.expect(['sudo'])
            child.sendline(password)                                                                                                                                             
        #child.logfile = sys.stdout.buffer #PY3
        child.logfile = fout # PY2                                                                                                                                                   
        child.expect(pexpect.EOF)                                                                                                                                                  
        child.close()                                                                                                                                                              
        fout.close()                                                                                                                                                               
    
        fin = open(fname, 'r')                                                                                                                                                     
        stdout = fin.read()                                                                                                                                                        
        fin.close()                                                                                                                                                                
    
        if 0 != child.exitstatus:                                                                                                                                                  
            raise Exception(stdout)                                                                                                                                             
        elif 'Invalid' in stdout:
            raise Exception(stdout)
        
        return stdout

    
    #command = ssh_command_string('172.18.1.111', as_string='while read p; do echo $p; done </proc/stonegate/name_cache/names')
    #command = ssh_command_string('172.18.1.111', as_string='while read -r ve_id group remaining; do if [[ $ve_id == V:* ]]; then echo "$ve_id $group"; fi; done </proc/stonegate/name_cache/names')
    
    def name_cache_command():
        return "awk '!seen[$1,$2]++' /proc/stonegate/name_cache/names | awk '$1 ~ /^V:/ {print $1,$2}'"
    
    command = ssh_command_string('172.18.1.111', as_string=name_cache_command())
    
    
    def get_name_cache(container, force_ssh=False):
        # Only get from first container, all nodes should have identical caches
        node = container.nodes.get(0)
        result = []
        try:
            if not force_ssh and 'dynamic_element_update' in node.data.links:
                pass
            else:
                ipaddr = getattr(node, 'vss_node_isc', {}).get('management_ip')
                command_string = ssh_command_string(
                    ipaddr, as_string=name_cache_command())
                
                stdout = run_ssh_command(command_string) or []
                logger.debug('SSH command get stdout: %s', stdout)
                for entry in stdout.replace('\r', '').split('\n'):
                    if entry:
                        v_colon, group = entry.split()
                        result.append((v_colon.split(':')[-1], group))

        except Exception as e:
            logger.error("Failed fetching name cache on container node: %s, %s",
                node, str(e))
        finally:
            return result
                
    
    sys.exit(1)
    
    from smc.core.name_cache import SecGroup
    
    secgroup = SecGroup()
    #secgroup.purge(ve_id=1)
    #secgroup.purge()
    #secgroup.purge()
    #secgroup.update('foo', '2.2.2.2', 1)
    #secgroup.update('foo3', '3.3.3.3', 1)
    #secgroup.update('foo2', '2.2.2.3', 2)
    #secgroup.remove('foo3', address='3.3.3.3', ve_id=1)
    secgroup.fetch(name='securitygroup-18')
    #print(secgroup.as_dict())
    
    # Test PURGE
    command = ssh_command_string('172.18.1.112', as_json=secgroup.as_dict())
    #print(command)
    #answer = run_ssh_command(command)
    
#     vss = VSSContainer('fooservice')
#     pprint(vars(vss.data))
#     
#     
#     for ctx in vss.vss_contexts:
#         print(ctx)    
#         
#     for sg in vss.security_groups:
#         print(sg)
#         pprint(vars(sg.data))
#     
    from smc.administration.system import System
    system = System()
     
    #clean_security_groups
    
    #EntryPoint(href=u'https://172.18.1.151:8082/6.5/system/visible_security_group_mapping', rel=u'visible_security_group_mapping', method=None)
    #EntryPoint(href=u'https://172.18.1.151:8082/6.5/system/clean_security_groups', rel=u'clean_security_groups', method=None)
    
    
   
    #print(get_context_status('fooservice'))
            
#     def create_vss_node(name, container, ip):
#         vss_node_def = {
#             'management_ip': ip,
#             'management_netmask': 24,
#             'isc_hypervisor': 'default',
#             'management_gateway': '172.18.1.254',
#             'contact_ip': ip}
#         return VSSContainerNode.create(name, container, vss_node_def,
#                                        comment='{}-{}'.format(name, ip))
#     
#     def create_vss_container(name):
#         vss_def = {
#             'isc_ovf_appliance_model': 'virtual',
#             'isc_ovf_appliance_version': '1.2.3.4.5',
#             'isc_ip_address': '192.168.4.151',
#             'isc_vss_id': 'service-123',
#             'isc_virtual_connector_name': 'serviceinstance-123'}
#         return VSSContainer.create(name, vss_def)
#     
#     create_vss_container('foobar')
#     create_vss_node(name='mynode', container=VSSContainer('foobar'), ip='1.1.1.1')
    
    
    sys.exit(1)
    
    
#     waiter = vss.upload('masterenginepol', wait_for_finish=True)
#     for x in range(0, 2):
#     #while not waiter.done():
#     #    waiter.wait(3)
# #     #    print("Try to create a container node while this guy is uploading!")   
#         waiter.wait(2)
#         print('first: %s' % vars(waiter.task.data))
#     
#     #waiter.task.abort()
#     #print("Aborted task....")
#      
#     waiter = vss.upload('masterenginepol', wait_for_finish=True)
#     while not waiter.done():
#         waiter.wait(2)
#         print('second: %s' % vars(waiter.task.data))
    

#     for tasks in TaskHistory():
#         if tasks.href == waiter.task.href:
#             task = tasks.task
#             print("Found Task: %s" % task)
#             if task.name == 'upload' and task.in_progress:
#                 print("Task is upload and in progress!")
    
    #TaskProgress.by_href()
    
    #ssh nsxadmin@172.18.1.111 -q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no "/usr/lib/stonegate/bin/test-name-cache-sockopt sgroup:securitygroup-18 172.18.1.21 99999999;/usr/lib/stonegate/bin/test-name-cache-sockopt sgroup:securitygroup-18 fe80::e982:d941:5b95:ba2c 99999999"
    
    
    sys.exit(1)
    
    
    security_groups = [{'name': 'securitygroup-18', 'friendly_name': u'endpoints', 'addresses': [u'172.18.1.21', u'fe80::e982:d941:5b95:ba2c'], 'action': 'update'}]
    for sg in security_groups:
        for addr in sg.get('addresses'):
            secgroup.update(name=sg.get('name'), address=addr, ve_id=1)
    

    # Security Group checks. We can get all NSX groups in a single query.
    # Currently rePOST with existing context takes
    # 3 groups
    # 2 virtual resources
    # 2x each group in NSX
            
        
    #print(get_containers_using_sg('endpoints'))
    
    
    data = {"type": "sec_group", "payload": [{"action": "update", "ve_id": 1, "name": "foo2", "timeout": "never", "address": "1.1.1.3"}]}
    
    secgrp = SecGroup()
    
    
    
    _container = VSSContainer('govcloud-service')
    #for node in vss.nodes:
    #    node.delete()
    
   

#     for container in VSSContainer.objects.all():
#         print("Container: %s groups: %s" % (container, mock_security_group_finder(container)))        
    
    #secgrp.update('test', address='23.23.23.23', ve_id=2)
    #secgrp.update('test2', address='24.24.24.24', ve_id=2)
    
#     secgrp.remove(name='test', ve_id=2)
#     
#     #secgrp.purge(name='test', ve_id=2)
#     vss.nodes.get(0).dynamic_element_update(secgrp)
#     
#     print(prepared_request(
#             href=vss.nodes.get(0).get_relation('dynamic_element_update'),
#             headers = {'content-type': 'multipart/form-data'},
#             files = {'update_file': serialized_json}).create())
#     
           
    def create_vss_node(name, container, ip):
        vss_node_def = {
            'management_ip': ip,
            'management_netmask': 24,
            'isc_hypervisor': 'default',
            'management_gateway': '172.18.1.254',
            'contact_ip': ip}
        return VSSContainerNode.create(name, container, vss_node_def,
                                       comment='{}-{}'.format(name, ip))
    
    def create_vss_container(name):
        vss_def = {
            'isc_ovf_appliance_model': 'virtual',
            'isc_ovf_appliance_version': '1.2.3.4.5',
            'isc_ip_address': '192.168.4.151',
            'isc_vss_id': 'service-123',
            'isc_virtual_connector_name': 'serviceinstance-123'}
        return VSSContainer.create(name, vss_def)
    
    create_vss_container('foocontainer')
    create_vss_node(name='mynode', container=VSSContainer('foocontainer'), ip='1.1.1.1')
    
    sg = ['securitygroup-18']
    
    
    def group_diff(group_callback, container):
        """
        Return groups that are unique to the NSX callback and need to
        be added by the VSS Container
        
        :param list(str) group_callback: list of groups from profile
        :param VSSContainer container: VSS container ref
        :rtype: tuple(list(remove), list(add))
        """
        container_sg = container.security_groups
        cgroups = [getattr(g, 'isc_id', None) for g in container_sg]
        
        remove = [g for g in cgroups if g not in group_callback]
        add = [g for g in group_callback if g not in cgroups]
        return remove, add
        

    revised_to = [u'securitygroup-10'] # IE removed
        
    v = VSSContainer('service')
    print(group_diff(revised_to, v))
    #[u'securitygroup-10', u'securitygroup-18']
    
    # Test removing a group!
    
    
    # TODO:
    # other than errors when trying to delete the other installations. Maybe do quick check and skip if not found
    # - Test add single node deployment, then come back and add another - the policy thread logic should take into
    ### consideration nodes that are already installed
    # - GUI delete option should forcibly delete all items, sometimes nodes are left around
    # Pause/Block when creating security policy if nodes are still initializing
    
    
#     v = VSSContainer.objects.filter('govcloud-dev').first()
#     for node in v.nodes:
#         pprint(vars(node.data))
#     ctr = create_vss_container('mytestcontainer')
#     create_vss_node(name='firstnode', container=ctr, ip='172.18.1.105')
#     create_vss_node(name='secondnode', container=ctr, ip='172.18.1.106')
    
                
    # security MAP returns:
    name_cache = [
        {'action': 'update', 'friendly_name': u'Activity Monitoring Data Collection', 'addresses': [], 'name': 'securitygroup-1'},
        {'action': 'update', 'friendly_name': u'Activity Monitoring Data Collection2', 'addresses': [], 'name': 'securitygroup-1'},
        {'action': 'update', 'friendly_name': u'Activity Monitoring Data Collection3', 'addresses': [], 'name': 'securitygroup-1'},
        {'action': 'update', 'friendly_name': u'Activity Monitoring Data Collection4', 'addresses': [], 'name': 'securitygroup-1'},
        {'action': 'update', 'friendly_name': u'Activity Monitoring Data Collection5', 'addresses': [], 'name': 'securitygroup-1'},]    
                 
    # BUGS  
    # Cannot VSS Container node
    # Cannot get VSS Container status
    
    
    session.logout()
    sys.exit(1)

    
    class HashableObject(object):
        __hash__ = None
        
        def __eq__(self, other):
            return False
        
        def __ne__(self, other):
            return not self == other
    
    
    class Foo(HashableObject):
        def __init__(self, name):
            self.name = name
        
        def __eq__(self, other):
            return self.name == other.name
        
        def __hash__(self):
            return hash((self.__class__.__name__, self.name))
        
        def __repr__(self):
            return 'Foo(name=%s)' % self.name
        
    
    foolist = [Foo('abc'), Foo('def'), Foo('ghi')]
    foolist2 = [Foo('def')]
    foolist3 = [Foo('abc'), Foo('def'), Foo('ghi')]

    print(set(foolist) ^ set(foolist2))
    print(set(foolist) ^ set(foolist3))
    
    class Bar(object):
        pass
    
    bar1 = Bar()
    bar2 = Bar()
    
    # Objects will compare equal by default and set's will compare equal
    # too based on default hash alone (based on ID by default), ie:
    # set(list1) ^ set(list2)
    # To make object comparison more precise to the object attributes,
    # implement __eq__, __ne__ (py2) and __hash__.
    
    
    
#     """
#     Good pattern
#     """
#     def __eq__(self, other):
#         return all([
#             self._api_key == getattr(other, '_api_key', None),
#             self._login == getattr(other, '_login', None),
#             self._pwd == getattr(other, '_pwd', None)
#         ])
# 
#     def __ne__(self, other):
#         return not self == other
    
#     from smc.administration.user_auth.users import InternalUserDomain, InternalUser, InternalUserGroup
#     domain = InternalUserDomain('InternalDomain') 
#     group = InternalUserGroup('abcdef')
   
    from smc.base.model import Element
    
    engine = Layer3Firewall('vm')
    
#     vpn = PolicyVPN('myvpn')
#     vpn.open()
#     #pprint(vars(vpn.data))
#     #print(list(vpn.central_gateway_node))
#         
#     vpn.data.update(mobile_vpn_topology_mode='Selected Gateway below')
#     vpn.update()
#     vpn.save()
#     vpn.add_mobile_gateway(engine)
#     #pprint(vars(vpn.data))
#     for gw in vpn.mobile_gateway_node:
#         pprint(vars(gw.data))
#     vpn.save()
#     vpn.close()
    
#     for mapping in engine.vpn_mappings:
#         print(mapping)
#         print("Is central: %s" % mapping.is_central_gateway)
#         print(mapping._central_gateway)
#         print(vars(mapping))
    
    from smc.elements.network import Host, Network
    from smc.base import transaction
    
#     with transaction.atomic():
#         Host.update_or_create(name='host3', address='1.1.1.1')
#         for name in range(1, 4):
#             Host.create(name='host%s' % name, address='1.1.1.1')
#     with Atomic(session):
#         for name in range(1, 10):
#             Host2.create(name='grace%s' % name, address='1.1.1.1')
#         
#         print("Now fail")
#         Host2.create(name='grace2', address='1.1.1.1')
#
    
    @transaction.atomic
    def mytasks():
        Host.update_or_create(name='host3', address='1.1.1.1')
        
        try:
            with transaction.atomic():
                for name in range(1, 4):
                    Host.create(name='host%s' % name, address='1.1.1.1')
        except Exception as e:
            print(vars(e))
            print("Transaction error ocurred: %s" % str(e))
            print(e.errors)
    
#     with transaction.atomic() as tx:
#         Host.create(name='host34', address='1.1.1.1')
#         print(tx._session.transactions)
#         tx.savepoint()
#         print(tx._session.transactions)
    
#     @transaction.atomic()
#     def mytasks():
#         for name in range(1, 4):
#             print("Deleting element: %s" % name)
#             try:
#                 Host('host%s' % name).delete()
#             except SMCException:
#                 pass
#         for name in range(1, 10):
#             print("Creating elemnt--> %s" % name)
#             Host.create(name='host%s' % name, address='1.1.1.1')
#          
#         Network.create(name='mynet2', ipv4_network='1.1.1.0/24')
#          
#         print("Now fail")
#         Host.create(name='grace10', address='1.1.1.1')
#         

#     proxy = ProxyServer('proxy')
#     pprint(vars(proxy.data))
#     
#     ProxyServer.update_or_create(name='proxy', address='1.1.1.1',
#                                  proxy_service="forcepoint_ap-web_cloud",
#                                  #fp_proxy_key = '12345',
#                                  comment = "Pre-mod comment")
    mytasks()
    session.logout()
    sys.exit(1)
        
    
#     with transaction.atomic():
#         for name in range(1, 5):
#             Host2.create(name='host%s' % name, address='1.1.1.1')
#         
#         with transaction.atomic():
#             print("Creating network!")
#             Network2.create(name='mynet3', ipv4_network='1.1.1.0/24')
#         
#         print("After exit out of inner: %s" % session.transactions)
#         print("Now fail")
#         #try:
#         Host2.create(name='grace132', address='1.1.1.1')
        #except SMCException as e:
        #    print("In exception: %s" % e)
        #    print(vars(session))
    
    print('----------->')
    
    #mytasks()

        
#     from smc.elements.network import Host
#     host = Host('host-172.18.1.20')
#     
    #patch(host.href, data=[{"op":"replace", "path": "/address", "value": "172.20.1.72"}],
    #      etag=host.etag)
    
#     engine = Engine('fw')
#     pprint(vars(engine.data))
#     r = session.session.get('https://172.18.1.151:8082/6.4/elements/single_fw/513?json_path=$.physicalInterfaces..physical_interface[?(@.interface_id == 0)]..link..href')
#     print(vars(r))

    
    
    # TODO: Change MTU on VLAN
    # Need to create __getattr__ and redirect these lookups
    # to self._parent as well as other methods
    
            
    #pprint(vars(engine.data))
    session.logout()
    sys.exit(1)
    
    class custom_setter(object):
        def __init__(self, func, doc=None):
            self.func = func
            self.__doc__ = doc if doc is not None else func.__doc__
        def __set__(self, obj, value):
            return self.func(obj, value)

    class element_list(object):
        def __init__(self, attr, doc=None):
            self.attr = attr
        def __set__(self, obj, value):
            elements = [element_resolver(elem) for elem in value]
            obj.data[self.attr] = elements
            return elements
        def __get__(self, obj, owner):
            return [obj.from_href(elem) for elem in obj.data.get(self.attr)]
            
    sentinel = object()
    
    import yaml  # @UnresolvedImport
    from smc.elements.network import Zone
    
    def zone_finder(zones, zone):
        for z in zones:
            if z.href == zone:
                return z.name
    
    from smc.vpn.policy import PolicyVPN
    def get_policy_vpn(engine):
        vpn_mappings = engine.vpn_mappings
        engine_internal_gw = engine.vpn.internal_gateway.name
        policy_vpn = []
        _seen = []
        if vpn_mappings:
            for mapping in vpn_mappings:
                mapped_vpn = mapping.vpn
                if mapped_vpn.name not in _seen:
                    _vpn = {'name': mapped_vpn.name}
                    vpn = PolicyVPN(mapped_vpn.name)
                    vpn.open()
                    nodes = vpn.central_gateway_node
                    node_central = nodes.get_contains(engine_internal_gw)
                    _vpn.update(central_node=True if node_central else False)
                    if not node_central: # If it's a central node it can't be a satellite node
                        nodes = vpn.satellite_gateway_node
                        _vpn.update(satellite_node=True if nodes.get_contains(engine_internal_gw) else False)
                    else:
                        _vpn.update(satellite_node=False)
                    if vpn.mobile_vpn_topology != 'None':
                        mobile_node = vpn.mobile_gateway_node
                        _vpn.update(mobile_gateway=True if mobile_node.get_contains(engine_internal_gw) else False)
                    
                    policy_vpn.append(_vpn)
                    vpn.close()
                    _seen.append(mapped_vpn.name)
        return policy_vpn
    
    
    engine = Engine('newcluster')
    print(get_policy_vpn(engine))
    session.logout()
    
    sys.exit(1)
    def yaml_cluster(engine):
        """
        Example interface dict created from cluster engine:
            
        
        Nodes dict key will always have at least `address`,
        `network_value` and `nodeid` if the interface definition
        has interface addresses assigned.
        """
        # Prefetch all zones to reduce queries
        zone_cache = list(Zone.objects.all())
        management = ('primary_mgt', 'backup_mgt', 'primary_heartbeat')
        yaml_engine = {'name': engine.name, 'type': engine.type}
        interfaces = []
        
        for interface in engine.interface:
            if not isinstance(interface, 
                (ClusterPhysicalInterface, Layer3PhysicalInterface, TunnelInterface)):
                continue
            top_itf = {}
            
            # Interface common settings
            top_itf.update(interface_id=interface.interface_id)
            
            if getattr(interface, 'macaddress', None) is not None:
                top_itf.update(macaddress=interface.macaddress)
            if getattr(interface, 'comment', None):
                top_itf.update(comment=interface.comment)
            if interface.zone_ref:
                top_itf.update(zone_ref=zone_finder(
                    zone_cache, interface.zone_ref))
            
            cvi_mode = getattr(interface, 'cvi_mode', None)
            if cvi_mode is not None and cvi_mode != 'none':
                top_itf.update(cvi_mode=interface.cvi_mode)
            
            if 'physical_interface' not in interface.typeof:
                top_itf.update(type=interface.typeof)
            
            if interface.has_interfaces:
                _interfaces = []    
                nodes = {}
                for sub_interface in interface.all_interfaces:
                    node = {}
                    if isinstance(sub_interface, ClusterVirtualInterface):
                        nodes.update(
                            cluster_virtual=sub_interface.address,
                            network_value=sub_interface.network_value)

                        # Skip remaining to get nodes
                        continue
                    else: # NDI
                        if getattr(sub_interface, 'dynamic', None):
                            node.update(dynamic=True, dynamic_index=
                                getattr(sub_interface, 'dynamic_index', 0))
                        else:
                            node.update(
                                address=sub_interface.address,
                                network_value=sub_interface.network_value,
                                nodeid=sub_interface.nodeid)
                            
                            for role in management:
                                if getattr(sub_interface, role, None):
                                    yaml_engine[role] = getattr(sub_interface, 'nicid')    

                    nodes.setdefault('nodes', []).append(node)
                
                if nodes:
                    _interfaces.append(nodes)
                if _interfaces:
                    top_itf.update(interfaces=_interfaces)
            
            elif interface.has_vlan:

                for vlan in interface.vlan_interface:
                    
                    itf = {'vlan_id': vlan.vlan_id}
                    if getattr(vlan, 'comment', None):
                        itf.update(comment=vlan.comment)
    
                    _interfaces = []    
                    nodes = {}
                    if vlan.has_interfaces:
                        for sub_vlan in vlan.all_interfaces:
                            node = {}
    
                            if isinstance(sub_vlan, ClusterVirtualInterface):
                                itf.update(
                                    cluster_virtual=sub_vlan.address,
                                    network_value=sub_vlan.network_value)
                                continue
                            else: # NDI
                                # Dynamic address
                                if getattr(sub_vlan, 'dynamic', None):
                                    node.update(dynamic=True, dynamic_index=
                                        getattr(sub_vlan, 'dynamic_index', 0))
                                else:
                                    node.update(
                                        address=sub_vlan.address,
                                        network_value=sub_vlan.network_value,
                                        nodeid=sub_vlan.nodeid)
    
                                for role in management:
                                    if getattr(sub_vlan, role, None):
                                        yaml_engine[role] = getattr(sub_vlan, 'nicid')
                
                            if vlan.zone_ref:
                                itf.update(zone_ref=zone_finder(
                                    zone_cache, vlan.zone_ref))
                            
                            nodes.setdefault('nodes', []).append(node)
                            
                        if nodes:
                            _interfaces.append(nodes)
                        if _interfaces:
                            itf.update(nodes)
                        
                        top_itf.setdefault('interfaces', []).append(itf)
                
                    else:
                        # Empty VLAN, check for zone
                        if vlan.zone_ref:
                            itf.update(zone_ref=zone_finder(
                                zone_cache, vlan.zone_ref))
                        
                        top_itf.setdefault('interfaces', []).append(itf)    
                        
            interfaces.append(top_itf)
            
        yaml_engine.update(
            interfaces=interfaces,
            default_nat=engine.default_nat.status,
            antivirus=engine.antivirus.status,
            file_reputation=engine.file_reputation.status,
            domain_server_address=[dns.value for dns in engine.dns
                                   if dns.element is None])
        if engine.comment:
            yaml_engine.update(comment=engine.comment)
    
        # Only return the location if it is not the default (Not set) location
        location = engine.location
        if location:
            yaml_engine.update(location=location.name)
        # Show SNMP data if SNMP is enabled
        if engine.snmp.status:
            snmp = engine.snmp
            data = dict(snmp_agent=snmp.agent.name)
            if snmp.location:
                data.update(snmp_location=snmp.location)
            interfaces = snmp.interface
            if interfaces:
                data.update(snmp_interface=[itf.interface_id for itf in interfaces])
            yaml_engine.update(snmp=data)
        
        if getattr(engine, 'cluster_mode', None):
            yaml_engine.update(cluster_mode=engine.cluster_mode)
        
        # BGP Data
        bgp = engine.bgp
        data = dict(enabled=bgp.status,
                    router_id=bgp.router_id)
        
        if bgp.status:    
            as_element = bgp.autonomous_system
            autonomous_system=dict(name=as_element.name,
                                   as_number=as_element.as_number,
                                   comment=as_element.comment)
            data.update(autonomous_system=autonomous_system)
            
            bgp_profile = bgp.profile
            if bgp_profile:
                data.update(bgp_profile=bgp_profile.name)
            
            antispoofing_map = {}
            for net in bgp.antispoofing_networks:
                antispoofing_map.setdefault(net.typeof, []).append(
                    net.name)
            antispoofing_network = antispoofing_map if antispoofing_map else {}
            data.update(antispoofing_network=antispoofing_network)
                
            announced_network = []
            for announced in bgp.advertisements:
                element, route_map = announced
                d = {element.typeof: {'name': element.name}}
                if route_map:
                    d[element.typeof].update(route_map=route_map.name)
                announced_network.append(d)
            data.update(announced_network=announced_network)
            
        yaml_engine.update(bgp=data)
        bgp_peering = []
        for interface, network, peering in engine.routing.bgp_peerings:
            peer_data = {}
            peer_data.update(interface_id=interface.nicid,
                             name=peering.name)
            if network:
                peer_data.update(network=network.ip)
            for gateway in peering:
                if gateway.routing_node_element.typeof == 'external_bgp_peer':
                    peer_data.update(external_bgp_peer=gateway.name)
                else:
                    peer_data.update(engine=gateway.name)
            bgp_peering.append(peer_data)
        if bgp_peering:
            data.update(bgp_peering=bgp_peering)
        
        # Netlinks
        netlinks = []
        for netlink in engine.routing.netlinks:
            interface, network, link = netlink
            netlink = {'interface_id': interface.nicid,
                       'name': link.name}
                
            for gw in link:
                gateway = gw.routing_node_element
                netlink.setdefault('destination', []).append(
                    {'name': gateway.name, 'type': gateway.typeof})
            
            netlinks.append(netlink)
        if netlinks:
            yaml_engine.update(netlinks=netlinks)
        
        # Policy VPN mappings
        policy_vpn = get_policy_vpn(engine)
        if policy_vpn:
            yaml_engine.update(policy_vpn=policy_vpn)
        # Lastly, get tags
        tags = [tag.name for tag in engine.categories]
        if tags:
            yaml_engine.update(tags=tags)
        return yaml_engine    

    from smc.vpn.policy import PolicyVPN
    engine = Engine('newcluster')
    #pprint(yaml_cluster(engine))
    
    
    def update_policy_vpn(policy_vpn, engine):
        """
        Update the policy VPN. Provide a list of policy VPN
        dict and update if changed. Policy VPN list of dict
        looks like:
            [{'central_node': True,
              'mobile_gateway': True,
              'name': u'myVPN',
              'satellite_node': False,
              'vpn_profile': u'VPN-A Suite'}]

        :param list policy_vpn: dict of policy VPN
        :param Engine engine: engine reference
        """
        changed = False
        mappings = []
        for mapping in engine.vpn_mappings:
            if mapping.name not in mappings:
                mappings.append(mapping.name)
        
        for vpn in policy_vpn:
            if vpn.get('name') not in mappings:
                _vpn = PolicyVPN(vpn.get('name'))
                _vpn.open()
                if vpn.get('central_node', False):
                    #_vpn.add_central_gateway(engine)
                    pass
                elif vpn.get('satellite_node', False):
                    #_vpn.add_satellite_gateway(engine)
                    pass
                if vpn.get('mobile_gateway', False):
                    _vpn.add_mobile_vpn_gateway(engine)
                _vpn.save()
                _vpn.close()
                changed = True
            else: # Engine is already a member of this VPN
                _vpn = PolicyVPN(vpn.get('name'))
                _vpn.open()
                central = _vpn.central_gateway_node
                print("Central: %s" % central)
                print(vars(central))
                _vpn.save()
                _vpn.close()
            
    
    pvpn = [{'central_node': True,
             'mobile_gateway': False,
             'name': u'ttesst',
             'satellite_node': False}]
    
    from smc.policy.layer3 import FirewallPolicy
    policy = FirewallPolicy('TestPolicy')
    rule = policy.search_rule('@2097170')[0]
    
    
    
    session.logout()
    sys.exit(1)
    class ElementList(object):
        """
        Represents a an element collection that provides the ability
        to add or modify elements. Keeps a cache of the elements fetched
        and removes the ones that are operated on. Typically this is best
        hidden behind a property as it elements in this container will
        require fetching by href to serialize.
        """
        def __init__(self, elementlist):
            self._elements = elementlist
            self._result_cache = None
        
        def _fetch_all(self):
            if self._result_cache is None:
                self._result_cache = [Element.from_href(elem)
                    for elem in self._elements] 

        def __iter__(self):
            self._fetch_all() 
            return iter(self._result_cache) 
        
        def replace_all(self, elements):
            self._elements[:] = elements
        
        def insert(self, elements):
            """
            Insert elements that dont exist
            """
            print("self._elements start: %s" % self._elements)
            self._elements.extend([elem.href for elem
                in elements if elem not in self])
            print("self elem after: %s" % self._elements)
        
        def delete(self, elements):
            """
            Elements to remove if they exist
            """
            self._elements[:] = [elem.href for elem
                in self if elem not in elements]
            if len(self._elements) != len(self._result_cache):
                self._result_cache[:] = [elem for elem in self._result_cache
                    if elem.href in self._elements]
    
   
  
    #u = InternalUser.create(name='fooed4',user_dn='dc=mynewgroup3,domain=InternalDomain')
    #print(u)
    
    session.logout()
    sys.exit(1)
    
    
    #print(ExternalLdapUserDomain('myldapdomain').get_users(['cn=administrator,cn=users,dc=lepages,dc=local']))
    from pprint import pprint
    pprint(vars(foo.data))
    session.logout()
    sys.exit()
        
    print("Methods: %s" % rule.authentication_options.methods)
    print("auth: %s" % rule.authentication_options.require_auth)
    
    for user in rule.authentication_options.users:
        print("user: %s" % user)
        pprint(vars(user.data))
    
    session.logout()
    sys.exit(1)    
    
    #rule.authentication_options.users.append(
    rule.authentication_options.data.setdefault('users', []).append(
        'https://172.18.1.151:8082/6.4/elements/external_ldap_user_group/Y249YWRtaW5pc3RyYXRvcixjbj11c2VycyxkYz1sZXBhZ2VzLGRjPWxvY2FsLGRvbWFpbj1teWxkYXBkb21haW4=')
    
    #print("*** Before update: %s" % rule.authentication_options.users)
    print("******* Updating *********")
    pprint(vars(rule.data))
    rule.update()

        
    from smc.administration.user_auth.users import ExternalLdapUser
    for x in ExternalLdapUser.objects.all():
        print('user: %s' % x)
           
    class UserIDService(Element):
        typeof = 'user_id_service'
    
    class UserIDAgent(Element):
        typeof = 'user_identification_agent'
 
    #ZGM9bGVwYWdlcyxkYz1sb2NhbCxkb21haW49bXlsZGFwZG9tYWlu
    import base64
    code_string = base64.b64decode('ZGM9bGVwYWdlcyxkYz1sb2NhbCxkb21haW49bXlsZGFwZG9tYWlu')
    print('Decoded: %s' % code_string)
    print('Encoded: %s' % base64.b64encode('cn=administrator,cn=users,dc=lepages,dc=local,domain=myldapdomain'))
    
    encoded = base64.b64encode('cn=foobar,dc=lepages,dc=local,domain=myldapdomain')
    print(encoded)
    print("decode foobar: %s" % base64.b64decode('Y249Zm9vYmFyLGRjPWxlcGFnZXMsZGM9bG9jYWwsZG9tYWluPW15bGRhcGRvbWFpbg=='))

    #TODO: BUG in moving rules
#     from smc.policy.layer3 import FirewallPolicy
#     FirewallPolicy('TestPolicy3').delete()
#     policy = FirewallPolicy.get_or_create(name='TestPolicy3')
#     
#     rule = policy.fw_ipv4_access_rules.create(
#             name='foo')
#     policy.fw_ipv4_access_rules.create(name='foo2')
#     rule.update(rank=1.0)
# 
#     # Add a rule only using the MobileVPN
#     policy.fw_ipv4_access_rules.create(
#         name='mobilevpn',
#         sources='any',
#         destinations='any',
#         services='any',
#         action='enforce_vpn',
#         mobile_vpn=True)
#     
#     for x in policy.fw_ipv4_access_rules:
#         pprint(vars(x.data))
# # #  
#     rulesection = policy.fw_ipv4_access_rules.create_rule_section(name='mysection', add_pos=15)
#     foobarred = policy.search_rule('mobilevpn')[0]
#     pprint(vars(foobarred.data))
# #      
#     foobarred.move_rule_after(rulesection)
#     print("After move after")
#     #for num, rules in enumerate(policy.fw_ipv4_access_rules, 1):
#     #    print(num, rules)
# #    
#     for x in policy.fw_ipv4_access_rules:
#         pprint(vars(x.data))
#        
#     foobarred = policy.search_rule('mobilevpn')[0]
#     print("********** DATA AFTER CALLING ?after")
#     pprint(vars(foobarred.data))
# #     
#     rulesection = policy.search_rule('mysection')[0]
#     print("----------------------------------------")       
#     foobarred = policy.search_rule('mobilevpn')[0]
#     pprint(vars(foobarred.data))
#     print("Moving before....")
#     #rulesection = policy.search_rule('myrulesection')[0]
#    
#     foobarred.move_rule_before(rulesection)
#     print("After move after")
#     for num, rules in enumerate(policy.fw_ipv4_access_rules, 1):
#         pprint(vars(rules.data))        
#     foobarred = policy.search_rule('mobilevpn')[0]
    

    vpn = {
            "gateway_nodes_usage": {
                "central_gateway_node_ref": "http://localhost:8082/6.5/elements/vpn/5/gateway_tree_nodes/central/59",
                "satellite_gateway_node_ref": "http://localhost:8082/6.5/elements/vpn/5/gateway_tree_nodes/central/59",
                "mobile_gateway_node_ref": "http://localhost:8082/6.5/elements/vpn/5/gateway_tree_nodes/central/59",
            },
            "gateway_ref": "http://localhost:8082/6.5/elements/fw_cluster/1563/internal_gateway/59",
            "vpn_ref": "http://localhost:8082/6.5/elements/vpn/5"
            }

    session.logout()
    sys.exit(1)
    
    single_fw = {'antivirus': False,
                 'backup_mgt': u'1.2',
                 'bgp': {'bgp_peering': [{'external_bgp_peer': u'bgppeer',
                                          'interface_id': u'1000',
                                          'name': u'mypeering4'}],
                         'enabled': False,
                         'router_id': None},
                 'default_nat': False,
                 'domain_server_address': [u'8.8.8.8'],
                 'file_reputation': False,
                 'interfaces': [{'interface_id': u'15'},
                                {'interface_id': u'1000',
                                 'interfaces': [{'nodes': [{'address': u'90.90.90.71',
                                                            'network_value': u'90.90.90.0/24',
                                                            'nodeid': 1}]}],
                                 'type': 'tunnel_interface'},
                                #{'interface_id': u'6',
                                # 'interfaces': [{'nodes': [{'dynamic': True}]}]},
                                {'interface_id': u'5', 'zone_ref': u'management'},
                                {'interface_id': u'56',
                                 'interfaces': [{'comment': u'added by api',
                                                 'nodes': [{'address': u'56.56.56.56',
                                                            'network_value': u'56.56.56.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'56'}]},
                                {'interface_id': u'20',
                                 'interfaces': [{'nodes': [{'address': u'11.11.11.11',
                                                            'network_value': u'11.11.11.0/24',
                                                            'nodeid': 1}]}]},
                                {'interface_id': u'SWP_0'},
                                {'interface_id': u'50',
                                 'interfaces': [{'nodes': [{'address': u'50.50.50.1',
                                                            'network_value': u'50.50.50.0/24',
                                                            'nodeid': 1}]}]},
                                {'interface_id': u'49',
                                 'interfaces': [{'nodes': [{'address': u'49.49.49.49',
                                                            'network_value': u'49.49.49.0/24',
                                                            'nodeid': 1}]}]},
                                {'comment': u'foocomment',
                                 'interface_id': u'1008',
                                 'interfaces': [{'nodes': [{'address': u'13.13.13.13',
                                                            'network_value': u'13.13.13.0/24',
                                                            'nodeid': 1}]}],
                                 'type': 'tunnel_interface',
                                 'zone_ref': u'foozone'},
                                {'interface_id': u'4', 'interfaces': [{'vlan_id': u'4'}]},
                                {'interface_id': u'3',
                                 'interfaces': [{'nodes': [{'address': u'4.4.4.5',
                                                            'network_value': u'4.4.4.0/24',
                                                            'nodeid': 1},
                                                           {'address': u'4.4.4.4',
                                                            'network_value': u'4.4.4.0/24',
                                                            'nodeid': 1}]}]},
                                {'interface_id': u'2',
                                 'interfaces': [{'nodes': [{'address': u'12.12.12.10',
                                                            'network_value': u'12.12.12.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'8',
                                                 'zone_ref': u'foozone'}],
                                 'zone_ref': u'management'},
                                {'interface_id': u'1',
                                 'interfaces': [{'nodes': [{'address': u'2.2.2.2',
                                                            'network_value': u'2.2.2.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'1'},
                                                {'nodes': [{'address': u'3.3.3.3',
                                                            'network_value': u'3.3.3.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'2'}]},
                                {'interface_id': u'0',
                                 'interfaces': [{'nodes': [{'address': u'1.1.1.1',
                                                            'network_value': u'1.1.1.0/24',
                                                            'nodeid': 1}]}]},
                                {'interface_id': u'55',
                                 'interfaces': [{'nodes': [{'address': u'55.55.55.55',
                                                            'network_value': u'55.55.55.0/24',
                                                            'nodeid': 1}]}]},
                                {'comment': u'foo',
                                 'interface_id': u'1030',
                                 'interfaces': [{'nodes': [{'address': u'130.130.130.130',
                                                            'network_value': u'130.130.130.0/24',
                                                            'nodeid': 1}]}],
                                 'type': 'tunnel_interface',
                                 'zone_ref': u'myzone'},
                                {'interface_id': u'52',
                                 'interfaces': [{'nodes': [{'address': u'53.53.53.53',
                                                            'network_value': u'53.53.53.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'53'},
                                                {'comment': u'comment for interface 52',
                                                 'nodes': [{'address': u'52.52.52.52',
                                                            'network_value': u'52.52.52.0/24',
                                                            'nodeid': 1}],
                                                 'vlan_id': u'52'}]},
                                {'comment': u'comment for interface 49',
                                 'interface_id': u'51',
                                 'interfaces': [{'nodes': [{'address': u'51.51.51.1',
                                                            'network_value': u'51.51.51.0/24',
                                                            'nodeid': 1}]}]},
                                {'interface_id': u'1005',
                                 'interfaces': [{'nodes': [{'address': u'14.14.14.14',
                                                            'network_value': u'14.14.14.0/24',
                                                            'nodeid': 1}]}],
                                 'type': 'tunnel_interface'}],
                 'name': u'myfw2',
                 'primary_mgt': u'0',
                 'snmp': {'snmp_agent': u'testsnmp', 'snmp_interface': [u'3', u'2.8']}}
    
    #print(yaml.safe_dump(yaml_cluster(engine), default_flow_style=False, encoding=('utf-8')))

    ################################################################################
    
    inline_on_ips = {
        'interface_id': '20',
        'second_interface_id': '20',
        'interface': 'inline_ips_interface',
        'logical_interface_ref': 'interfaceref',
        'inspect_unspecified_vlans': True,
        'failure_mode': 'bypass',
        'interfaces': [{'logical_interface_ref': 'logical',
                        'vlan_id': 15,
                        'second_vlan_id': 17,
                        'zone_ref': 'vlan15 side a',
                        'second_zone_ref': 'vlan15 side b',
                        'comment': 'vlan15_comment'},
                        {'logical_interface_ref': 'logical2',
                         'vlan_id': 16}],
        'zone_ref': 'foozone',
        'second_zone_ref': 'foozone',
        'comment': 'mycomment'}
    

    engine = Engine('myfw')
    #TODO:
    # Remove getattr proxy from collections
    # Test InlineInterfaces with VLANs and delete
    # Tunnel interface routes are not removed after update and create when network changes - to_delete and invalid are not set when main interface is changed

    
    session.logout()
    sys.exit(1)
    
    
    #engine = Engine('newcluster')
    #itf = engine.interface.get(24)
    #pprint(itf.data.data)
    # External GW match is not exact: TODO:  BUG
    # GET /6.4/elements?filter=extgw4&filter_context=external_gateway&exact_match=True&case_sensitive=True
    # Returns: {"result":[{"href":"https://172.18.1.151:8082/6.4/elements/external_gateway/69","name":"extgw3","type":"external_gateway"}]}
    
    session.logout()
    sys.exit(1)
    
    # BUG: Cannot update NAT translation ports
    # Should be able to remove translation ports??
    
    #session.logout()
    #sys.exit(1)
    #rule = policy.search_rule('dstandsrcnat')
    #if rule:
    #    pprint(rule[0].data)
    #    print(rule[0].static_dst_nat.translated_ports)
        
    # Bug when destination cannot be resolved in NAT dest
    '''
    policy.fw_ipv4_nat_rules.create(
            name='dstandsrcnat',
            sources='any',
            destinations=[Host('kali')],
            services='any',
            dynamic_src_nat='5.5.5.10',
            static_dst_nat='3.3.3.3',
            static_dst_nat_ports=(22, 2222))
    '''
    
    
    #yaml_cluster(engine)
    #print(yaml.safe_dump(yaml_cluster(engine), default_flow_style=False, encoding=('utf-8')))                
    
   

    # Management to single IP on VLAN interface with multiple IPs    
    
    session.logout()
    sys.exit(1)

    import inspect
    def generic_type_dict(clazz):
        """
        Derive a type dict based on any element
        
        :param Element clazz: a class of type element
        :rtype: dict
        """
        types = dict()
        attr = inspect.getargspec(clazz.create).args[1:]
        types[clazz.typeof] = {'attr': attr}
        return types
    
    pprint(generic_type_dict(AutonomousSystem))
    
    engine = Engine('myfw')
    
    #TODO: Version 6.3.4 / 6.4
    
    # Filter for reports
    # ActiveAlerts
    #tls_profile
    #tls_inspection_policy
    #tls_cryptography_suite_set
    #for x in Search.objects.entry_point('tls_cryptography_suite_set'):
    #    pprint(x.data)
    
    
    class element(object):
        """
        Descriptor can be placed on a method that returns href's
        that should be resolved into Elements.
        """
        def __init__(self, fget):
            self.fget = fget
     
        def __get__(self, instance, owner=None):  # @UnusedVariable
            if instance is None:
                return self
            href = self.fget(instance)
            if isinstance(href, list):
                return [Element.from_href(ref) for ref in href]
            return Element.from_href(href)


    #IndexedIterable()
    #### 
    # Type Hint for eclipse
    # assert isinstance(policy.fw_ipv4_access_rules, IPv4Rule)
    
    
    # Interface should mask __getitem__ or just document that indexing is not supported?
    #   
    # decorator for deleting cache that handles exception raising in function
    # Rule needs an update method - clear _cache before calling
    # Need to rename 'addresses' and 'add_arp' in interfaces to avoid proxying these
    # override update on interface, remove save?
    # Consider this for property documentation:
    #     :getter: Returns this direction's name
    #     :setter: Sets this direction's name
    #     :type: string

  

    #session.logout()
    
    
    import smc.elements.network as network
    import smc.elements.group as group
    
    
    def network_elements():   
        types = dict(
            host=dict(type=network.Host),
            network=dict(type=network.Network),
            address_range=dict(type=network.AddressRange),
            router=dict(type=network.Router),
            ip_list=dict(type=network.IPList),
            group=dict(type=group.Group),
            interface_zone=dict(type=network.Zone),
            domain_name=dict(type=network.DomainName))
        
        for t in types.keys():
            clazz = types.get(t)['type']
            types[t]['attr'] = inspect.getargspec(clazz.create).args[1:]
        
        return types
    
    def ro_network_elements():
        types = dict(
            alias=dict(type=network.Alias),
            country=dict(type=network.Country),
            expression=dict(type=network.Expression),
            engine=dict(type=Engine))
    
        for t in types.keys():
            clazz = types.get(t)['type']
            types[t]['attr'] = inspect.getargspec(clazz.__init__).args[1:]
        
        return types
    
    ELEMENT_TYPES = network_elements()
    ELEMENT_TYPES.update(ro_network_elements())

    
    #g = Group('group_referencing_existing_elements')
    #print([x.href for x in g.obtain_members()])
    #pprint(element_dict_from_obj(g, ELEMENT_TYPES, expand=['group']))
    
    # All other elements use name/comments to search
    SEARCH_HINTS = dict(
        network='ipv4_network',
        address_range='ip_range',
        host='address',
        router='address'
    )
    
    def is_element_valid(element, type_dict, check_required=True):
        """
        Are all provided arguments valid for this element type.
        Name and comment are valid for all.
        
        :param dict element: dict of element
        :param bool check_required: check required validates that at least
            one of the required arguments from the elements `create` constructor
            is provided. This is set to True when called from the network_element
            or service_element modules. This can be False when called from the
            firewall_rule module which allows an element to be fetched only.
        :return: None
        """
        for key, values in element.items():
            if not key in type_dict:
                return 'Unsupported element type: {} provided'.format(key)
    
            valid_values = type_dict.get(key).get('attr', [])

            # Verify that all attributes are supported for this element type
            provided_values = values.keys() if isinstance(values, dict) else []
            if provided_values:
                # Name is always required
                if 'name' not in provided_values:
                    return 'Entry: {}, missing required name field'.format(key)
            
                for value in provided_values:
                    if value not in valid_values:
                        return 'Entry type: {} with name {} has an invalid field: {}. '\
                            'Valid values: {} '.format(key, values['name'], value, valid_values)
                
                if check_required:
                    required_arg = [arg for arg in valid_values if arg not in ('name', 'comment')]
                    if required_arg: #Something other than name and comment fields
                        if not any(arg for arg in required_arg if arg in provided_values):
                            return 'Missing a required argument for {} entry: {}, Valid values: {}'\
                                .format(key, values['name'], valid_values)
                
                if 'group' in element and values.get('members', []):
                    for element in values['members']:
                        if not isinstance(element, dict):
                            return 'Group {} has a member: {} with an invalid format. Members must be '\
                                'of type dict.'.format(values['name'], element)
                        invalid = is_element_valid(element, type_dict, check_required=False)
                        if invalid:
                            return invalid
            else:
                return 'Entry type: {} has no values. Valid values: {} '\
                    .format(key, valid_values)
        
    
    elements = [
                {
                    "address": "1.1.1.1", 
                    "host": "foobar4562"
                }, 
                {
                    "comment": "foo",
                    "ipv4_network": "1.1.0.0/24",
                    "network": "foonetwork1.2.3"
                },
                {
                    "network": "any"
                },
                {
                    "address_range": "myrange3", 
                    "ip_range": "3.3.3.1-3.3.3.5"
                }, 
                {
                        "address": "172.18.1.254", 
                        "ipv6_address": "2003:dead:beef:4dad:23:46:bb:101", 
                        "router": "myrouter2", 
                        "secondary": [
                            "172.18.1.253"
                        ]
                },
                {
                    "alias": "$ EXTERNAL_NET",
                }, 
                {
                    "domain_name": "dogpile.com",
                    "comment": "bar"
                }, 
                {
                    "interface_zone": "external_zone123"
                },
                {
                    "interface_zone": "new123zone",
                    "comment": "dingo"
                },
                {
                    "ip_list": "mylist",
                    "iplist": ['45.45.45.45']
                }, 
                {
                    "group": "doodoo",
                    "members": [
                        {'host': {'name':'blah'}
                        }]
                }, 
                {
                    "country": [
                        "Armenia", 
                        "United States", 
                        "China"
                    ]
                }, 
                {
                    "engine": [
                        "fw2", 
                        "myfirewall"
                    ]
                }
            ]            
    
    
    NETWORK_ELEMENTS = ELEMENT_TYPES.keys()
    
    
    def extract_element(element, type_dict):
        """
        Extract a dict like yml entry. Split this into a dict in
        the correct format if the element type exists.
        """
        key = [key for key in set(element) if key in type_dict]
        if key and len(key) == 1:
            typeof = key.pop()
            element['name'] = element.pop(typeof)
            return typeof, {typeof: element}

    def is_field_any(field):
        """
        Is the source/destination or service field using an ANY
        value.
        
        :rtype: bool
        """
        if 'network' in field and field['network']['name'].upper() == 'ANY':
            return True
        return False
    
    def update_or_create(element, type_dict, hint=None, check_mode=False):
        """
        Create or get the element specified. The strategy is to look at the
        element type and check the default arguments. Some elements require
        only name and comment to create. Others require specific arguments.
        If only name and comment is provided and the constructor requires
        additional args, try to fetch the element, otherwise call
        get_or_create. If the constructor only requires name and comment,
        these will also call get_or_create.
        
        :param dict element: element dict, key is typeof element and values
        :param dict type_dict: type dict mappings to get class mapping
        :param str hint: element attribute to use when finding the element
        :raises CreateElementFailed: may fail due to duplicate name or other
        :raises ElementNotFound: if fetch and element doesn't exist
        :return: The result as type Element
        """
        for typeof, values in element.items():
            type_dict = type_dict.get(typeof)
            
            filter_key = {hint: values.get(hint)} if hint in values else None
            raise_exc = False if check_mode else True
            
            if check_mode:
                result = type_dict['type'].get(values.get('name'), raise_exc)
                if result is None:
                    return dict(
                        name=values.get('name'),
                        type=typeof,
                        msg='Specified element does not exist')
            else:
                attr_names = type_dict.get('attr', []) # Constructor args
                provided_args = set(values)
                
                # Guard against calling update_or_create for elements that
                # may not be found and do not have valid `create` constructor
                # arguments
                if set(attr_names) == set(['name', 'comment']) or \
                    any(arg for arg in provided_args if arg not in ('name',)):
                    
                    result = type_dict['type'].update_or_create(filter_key=filter_key, **values)
                else:
                    print("Only perform GET!")
                    result = type_dict['type'].get(values.get('name'))

                return result
            
            
    def get_or_create_element(element, type_dict, hint=None, check_mode=False):
        """
        Create or get the element specified. The strategy is to look at the
        element type and check the default arguments. Some elements require
        only name and comment to create. Others require specific arguments.
        If only name and comment is provided and the constructor requires
        additional args, try to fetch the element, otherwise call
        get_or_create. If the constructor only requires name and comment,
        these will also call get_or_create.
        
        :param dict element: element dict, key is typeof element and values
        :param dict type_dict: type dict mappings to get class mapping
        :param str hint: element attribute to use when finding the element
        :raises CreateElementFailed: may fail due to duplicate name or other
        :raises ElementNotFound: if fetch and element doesn't exist
        :return: The result as type Element
        """
        for typeof, values in element.items():
            type_dict = type_dict.get(typeof)
    
        # An optional filter key specifies a valid attribute of
        # the element that is used to refine the search so the
        # match is done on that exact attribute. This is generally
        # useful for networks and address ranges due to how the SMC
        # interprets / or - when searching attributes. This changes
        # the query to use the attribute for the top level search to
        # get matches, then gets the elements attributes for the exact
        # match. Without filter_key, only the name value is searched.
        filter_key = {hint: values.get(hint)} if hint in values else None
        
        if check_mode:
            #print(type_dict['type'].get(values.get('name')))
            #result = type_dict['type'].get(values.get('name'), raise_exc=False)
            print("Filter key: %s" % filter_key)
            if filter_key:
                print("Via filter key: %s" % filter_key)
                result = type_dict['type'].objects.filter(**filter_key).first()
            else:
                print("No filter")
                result = type_dict['type'].objects.filter(values.get('name')).first()
            print("Result: %s" % result)
            if result is None:
                return dict(
                    name=values.get('name'),
                    type=typeof,
                    msg='Specified element does not exist')
        else:
            result = type_dict['type'].get_or_create(filter_key=filter_key, **values)
            return result
    
    print(get_or_create_element({'autonomous_system': {'name': 'fooas', 'as_number': '100'}},
                                 {'autonomous_system': {'type': AutonomousSystem}}, hint='as_number', check_mode=True))
    
    
    #import timeit
    #print(timeit.repeat("test()",
    #                    setup="from __main__ import test", number=1000000,
    #                    repeat=3))

    #tls = TLSServerCredential.create(name='tlstest', common_name="CN=myserver.lepages.local")
    #tls = TLSServerCredential('LePagesCA')
    #pprint(tls.data)
    
    
    print(vars(session))
    #c = copy.copy(session)
    #print("Copy of...")
    #print(vars(c))
    print("Switch domain to nsx.....")
    session.switch_domain('nsx')
    print(vars(session))
    print(session.domain)
    
    #print("copied instance after switching domains: %s" % vars(c))
    result = SMCRequest(params={'filter_context': 'single_fw',
                                'exact_match': False,
                                'domain': 'nsx'}).read()
    print(result)
    for x in session.entry_points.all():
        if 'tls' in x:
            print(x)

    engine = Engine('bar')
    pprint(engine.data)
    
    #ClientProtectionCA.create('foo')
    print(engine.server_credential)
        
    #    print(x.certificate_export())

        
        
        
    
    # Daily
    {'day_period': 'daily',
     'minute_period': 'hourly', # every hour
     'minute_period': 'each_half', # each half hour
     'minute_period': 'each_quarter'} # every 15 minutes
    
    # Weekly - I cant figure out the day mask
    {'day_period': 'weekly',
     'minute_period': 'one_time',
     'day_mask': 124 # Mon - Friday
     }
    
    # Monthly
    {'day_period': 'monthly',
     'minute_period': 'one_time'}
    
    # Yearly
    {'day_period': 'yearly',
     'minute_period': 'one_time'}
    
    a = {u'activated': True,
         u'activation_date': '2017-10-04T09:33:09.890000-05:00',
         u'comment': u'test',
         u'day_mask': 0,
         u'day_period': u'one_time',
         u'final_action': u'ALERT_FAILURE',
         u'minute_period': u'one_time',
         u'name': u'test7'}
    
    #b = prepared_request(href='https://172.18.1.151:8082/6.3/elements/refresh_policy_task/42/task_schedule',
    #                     json=a).create()
    #print(b)
    
    '''
    export_log_task
    archive_log_task
    remote_upgrade_task
    '''
    #client_gateway
    #validate_policy_task
    #refresh_policy_task
    
    #print(get_options_for_link('https://172.18.1.151:8082/6.3/elements/fw_alert'))
    
         
    import pexpect  # @UnresolvedImport
    import tempfile
   
    def ssh(host, cmd, user, password, timeout=15, bg_run=False):                                                                                                 
        """SSH'es to a host using the supplied credentials and executes a command.                                                                                                 
        Throws an exception if the command doesn't return 0.                                                                                                                       
        bgrun: run command in the background"""                                                                                                                                    
    
        fname = tempfile.mktemp()                                                                                                                                                  
        fout = open(fname, 'w')                                                                                                                                                    
    
        options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'                                                                         
        if bg_run:                                                                                                                                                         
            options += ' -f'                                                                                                                                                       
        ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
        print("SSH CMD: %s" % ssh_cmd)                                                                                                               
        child = pexpect.spawn(ssh_cmd, timeout=timeout)
        
        #child.expect(['[sudo] password for nsxadmin: '])
        #child.sendline(password)
        child.expect(['Password: '])                                                                                                                                                                                                                                                                                               
        child.sendline(password)
        if 'sudo' in ssh_cmd:
            child.expect(['sudo'])
            child.sendline(password)                                                                                                                                          
        #child.logfile = fout
        child.logfile = sys.stdout.buffer                                                                                                                                                      
        child.expect(pexpect.EOF)                                                                                                                                                  
        child.close()                                                                                                                                                              
        fout.close()                                                                                                                                                               
    
        fin = open(fname, 'r')                                                                                                                                                     
        stdout = fin.read()
        fin.close()                                                                                                                                                                
    
        if 0 != child.exitstatus:                                                                                                                                                  
            raise Exception(stdout)                                                                                                                                                
    
        return stdout
    
    
    cmd = 'sudo -u root -S msvc -r dpa'
    #print(ssh('172.18.1.111', cmd=cmd, user='nsxadmin', password='password'))
    

    
    from smc.administration.system import System
    for x in Search.objects.entry_point('tls_server_credentials').all():
        if x.name == 'lepages':
            pprint(x.data)

   
            
    
    
    class ProbingProfile(Element):
        typeof = 'probing_profile'
        def __init__(self, name, **meta):
            super(ProbingProfile, self).__init__(name, **meta)
    
    class ThirdPartyMonitoring(object):
        def __init__(self, log_server=None, probing_profile=None,
                     netflow=False, snmp_trap=False):

            if not log_server:
                log_server = LogServer.objects.first()

            self.monitoring_log_server_ref = element_resolver(log_server)

            if not probing_profile:
                probing_profile = ProbingProfile.objects.filter('Ping').first()

            self.probing_profile_ref = element_resolver(probing_profile)

            self.netflow = netflow
            self.snmp_trap = snmp_trap

        def __call__(self):
            return vars(self)



    #host.third_party_monitoring = ThirdPartyMonitoring()
    #print(vars(host))
    #host.update()

    #t = ThirdPartyMonitoring()
    #host.third_party_monitoring = t

    #print("Finished polling, result is: %s" % poller.result())
    vss_def = {"isc_ovf_appliance_model": 'virtual',
               "isc_ovf_appliance_version": '',
               "isc_ip_address": '1.1.1.1',
               "isc_vss_id": 'foo',
               "isc_virtual_connector_name": 'smc-python'}

    vss_node_def = {
            'management_ip': '4.4.4.6',
            'management_netmask': '24',
            'isc_hypervisor': 'default',
            'management_gateway': '2.2.2.1',
            'contact_ip': None}
    '''
    rbvpn_tunnel_side
    rbvpn_tunnel_monitoring_group
    rbvpn_tunnel
    '''
  
    
    
            
    '''
    by_action = {
        "format": {
            "type": "texts",
            "field_ids": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": LogField.ACTION},
                "right":[
                    {"type": "constant", "value":Actions.DISCARD}]}
        },
        "fetch":{"quantity":100}
    }
    
    by_protocol = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": "Protocol"
                },
                "right":[{
                    "type": "number",
                    "value":6}]
            }
        },
        "fetch":{"quantity":100}
    }
    
    by_service = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": "Service"},
                "right":[
                    {"type": "service",
                     "value": "TCP/80"}]
            }
        },
        "fetch":{"quantity":100}
    }
    
    by_sender = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "id",
                    "name": LogField.SRC},
                "right":[
                    {"type": "ip",
                     "value": "1.1.1.1"}]
            }
        },
        "fetch":{"quantity":100}
    }

    ip_and_service = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "start_ms": 0,
            "end_ms": 0,
            "filter": {
                "type": "and",
                "values": [
                    {"type": "in",
                     "left": {
                         "type": "field",
                         "name": "Service"},
                     "right":[
                         {"type": "service",
                          "value": "TCP/443"}]
                    },
                    {"type": "in",
                     "left": {
                         "type": "field",
                         "id": LogField.SRC},
                     "right":[
                         {"type": "ip",
                          "value": "192.168.4.84"}]
                    },       
                    ]
            }
        },
        "fetch":{"quantity":100}
    }
    
    
    cs_like_filter = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "ci_like",
                "left": {
                    "type": "field",
                    "id": LogField.INFOMSG},
                "right": {
                    "type": "string", 
                    "value":"Connection was reset by client" }
                }
        },
        "fetch":{"quantity":100}
    }
    
    bl2 = {
        'fetch': {},
        'format': {
            "type": "texts",
            "field_format": "name",
            "resolving": {
                "senders": True}
        },
        'query': {
            'definition': 'BLACKLIST', 
            'target': 'sg_vm'}
    }
    
    blacklist = {
        'fetch': {},
        'format': {
            'type': 'combined',
            'formats': {
                "fields": {
                    "type": "detailed",
                    "field_format": "name"
                },
                "bldata": {
                    "type": "texts",
                    "field_format": "name",
                    "resolving": {"time_show_zone": True,
                                  "timezone": "CST"
                    }
                },
                "blentry": {
                    "type": "texts",
                    "field_format": "pretty",
                    "field_ids": [LogField.BLACKLISTENTRYID]
                }
            }
        },
        'query': {
            'definition': 'BLACKLIST', 
            'target': 'sg_vm'}
    }
    '''
    '''
    ids = resolve_field_ids(list(range(1000)))
    for x in ids:
        pprint(x)
    for x in reversed(ids):
        print('{}={} #: {}'.format(
            x.get('name').upper(),
            x.get('id'),
            x.get('comment')))

    sys.exit(1)
    '''
    
    
    
    #import timeit
    #print(timeit.repeat("{link['rel']:link['href'] for link in links}",
    #                    setup="from __main__ import links", number=1000000,
    #                    repeat=3))
    
    #import timeit
    # print(timeit.timeit("ElementFactory('http://172.18.1.150:8082/6.1/elements/host/978')",
    # setup="from __main__ import ElementFactory", number=1000000))

    #print(timeit.timeit("find_link_by_name('self', [])", setup="from smc.base.util import find_link_by_name"))


    print(time.time() - start_time)
    session.logout()

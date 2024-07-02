from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions

from huaweicloudsdkcce.v3 import *
from huaweicloudsdkcce.v3.region.cce_region import CceRegion

from huaweicloudsdkecs.v3 import *
from huaweicloudsdkecs.v3.region.ecs_region import EcsRegion

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def handler(event, context):
    
    project_id = context.getUserData('projectId', '').strip()
    cce_endpoint = context.getUserData('cce_endpoint', '').strip()
    ecs_endpoint = context.getUserData('ecs_endpoint', '').strip()
    region = context.getUserData('region', '').strip()
    ak = context.getAccessKey().strip()
    sk = context.getSecretKey().strip()
    instruct_type = context.getUserData('type', '').strip()
    white_list = context.getUserData('whiteLists', '').strip().split(',')
    
    if not project_id:
        raise Exception("'project_id' not configured")
    
    if not region:
        raise Exception("'region' not configured")
    
    if not white_list:
        raise Exception("'whiteLists' not configured")
    
    if not instruct_type:
        instruct_type = "SOFT"
    
    if not ak or not sk:
        ak = context.getUserData('ak', '').strip()
        sk = context.getUserData('sk', '').strip()
        if not ak or not sk:
            raise Exception("ak/sk empty")
    
    logger = context.getLogger()
    
    credentials = BasicCredentials(ak, sk).with_project_id(project_id)
    
    if cce_endpoint and ecs_endpoint:
        cce_client = CceClient.new_builder() \
            .with_credentials(credentials) \
            .with_endpoint(cce_endpoint) \
            .build()
        
        ecs_client = EcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_endpoint(ecs_endpoint) \
            .build()
        
    else:
        cce_client = CceClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CceRegion.value_of(region)) \
            .build()
        
        ecs_client = EcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(EcsRegion.value_of(region)) \
            .build()
        
    try:
        # This is from the CceClient. We need to get the nodes.
        request = ListNodesRequest()
        response = cce_client.list_nodes(request)
        print(response)
        
        # This is from the EcsClient. We need to send a request to stop the nodes.
        # request = BatchStopServersRequest()
        # response = ecs_client.batch_stop_servers(request)
        # print(response)
    
    except exceptions.ClientRequestException as e:
        logger.error(e.status_code)
        logger.error(e.request_id)
        logger.error(e.error_code)
        logger.error(e.error_msg)

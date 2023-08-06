# coding=utf-8
from __future__ import print_function
import uuid

from src.cloud_foundry import CloudFoundry
from src.resource_controller import ResourceController, RESOURCE_ID_AIOPENSCALE, PLAN_ID_AIOPENSCALE, RESOURCE_ID_MACHINE_LEARNING, PLAN_ID_MACHINE_LEARNING
from src.setup_services import SetupIBMCloudServices
from src.token_manager import TokenManager
from src.utils import jsonFileToDict


class SetupIBMCloudServicesRest(SetupIBMCloudServices):

    def __init__(self, args, environment):
        super().__init__(args, environment)
        iam_access_token = TokenManager(
            apikey=args.apikey,
            url=environment['iam_url']
        ).get_token()
        self.resourceController = ResourceController(
            access_token=iam_access_token,
            url=environment['resource_controller_url'],
            resourceGroupUrl=environment['resource_group_url']
        )
        uaa_access_token = TokenManager(
            apikey=args.apikey,
            url=environment['uaa_url'],
            iam_token=False
        ).get_token()
        self.cloudFoundry = CloudFoundry(access_token=uaa_access_token)

    def _getCredentials(self, params, isRCBased, credentialsFile=None):
        '''
        Returns the credentials from the specified credentials json file. If not
        then returns the credentials an instance of the specified Service.
        If there is no instance available, a new one is provisioned.
        If there are no existing credentials, new one is created and returned.
        '''
        print('Setting up {} instance'.format(
            params['service_display_name']))
        credentials = None

        if credentialsFile is not None and credentialsFile.strip():
            print('\t - Credentials file specified')
            credentials = jsonFileToDict(credentialsFile.strip())
            print('\t - Using credentials from "{}"'.format(credentialsFile))
        else:
            if isRCBased:
                credentials = self.resourceController.get_or_create_instance(
                    resource_id=params['resource_id'],
                    resource_name=params['instance_name'],
                    resource_plan_id=params['resource_plan_id'],
                    resource_group_name=self.args.resource_group,
                    create_credentials=params['create_credentials']
                )
            else:
                credentials = self.cloudFoundry.get_or_create_instance(
                    service_name=params['service_name'],
                    service_instance_name=params['instance_name'],
                    service_plan_guid=params['service_plan_guid'],
                    organization_name=self.args.organization,
                    space_name=self.args.space
                )
        return credentials

    def setupAIOS(self):
        aiopenscale_params = {}
        aiopenscale_params['service_display_name'] = 'AI OpenScale'
        aiopenscale_params['instance_name'] = 'aiopenscale-fastpath-instance'
        aiopenscale_params['resource_id'] = RESOURCE_ID_AIOPENSCALE
        aiopenscale_params['resource_plan_id'] = PLAN_ID_AIOPENSCALE
        aiopenscale_params['create_credentials'] = False
        aios_instance = self._getCredentials(aiopenscale_params, True)
        aios_credentials = {}
        if self.args.env[:3].lower() == 'icp':
            aios_credentials['data_mart_id'] = uuid.uuid4()
            aios_credentials['url'] = self.environment['aios_url']
        else:
            aios_credentials['data_mart_id'] = aios_instance['id']
            aios_credentials['apikey'] = self.args.apikey
            aios_credentials['url'] = self.environment['aios_url']
        return aios_credentials

    def setupWML(self):
        wml_params = {}
        wml_params['service_display_name'] = 'Watson Machine Learning'
        wml_params['instance_name'] = 'wml-fastpath-instance'
        wml_params['resource_id'] = RESOURCE_ID_MACHINE_LEARNING
        wml_params['resource_plan_id'] = PLAN_ID_MACHINE_LEARNING
        wml_params['create_credentials'] = True
        if self.args.wml is not None:
            return self._getCredentials(wml_params, True, self.args.wml)
        return self._getCredentials(wml_params, True)['credentials']

    def setupPostgresDatabase(self):
        postgres_params = {}
        postgres_params['service_display_name'] = 'Compose for PostgreSQL'
        if self.args.postgres is not None:
            return self._getCredentials(postgres_params, False, self.args.postgres)
        print('Setting up AIOS internal database')
        return None

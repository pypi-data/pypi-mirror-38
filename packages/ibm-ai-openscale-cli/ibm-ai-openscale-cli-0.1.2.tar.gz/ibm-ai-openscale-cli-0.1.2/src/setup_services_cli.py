# coding=utf-8
from __future__ import print_function
import uuid
from src.cloud_foundry_cli import getCFInstanceCredentials
from src.resource_controller_cli import getRCInstanceCredentials
from src.setup_services import SetupIBMCloudServices
from src.utils import jsonFileToDict


class SetupIBMCloudServicesCli(SetupIBMCloudServices):

    def _getCredentials(self, params, isRCBased, credentialsFile=None):
        '''
        Returns the credentials from the specified credentials json file. If not
        then returns the credentials an instance of the specified Service.
        If there is no instance available, a new one is provisioned.
        If there are no existing credentials, new one is created and returned.
        '''
        print('Setting up {} instance'.format(params['service_display_name']))
        credentials = None
        if credentialsFile is not None and credentialsFile.strip():
            print('\t - Credentials file specified')
            credentials = jsonFileToDict(credentialsFile.strip())
            print('\t - Using credentials from "{}"'.format(credentialsFile))
        else:
            if isRCBased:
                credentials = getRCInstanceCredentials(params)
            else:
                credentials = getCFInstanceCredentials(params)
        return credentials

    def setupAIOS(self):
        aiopenscale_params = {}
        aiopenscale_params['service_display_name'] = 'AI OpenScale'
        aiopenscale_params['service_name'] = 'aiopenscale'
        aiopenscale_params['instance_name'] = 'aiopenscale-fastpath-instance'
        aiopenscale_params['service_plan_name'] = 'lite'
        aiopenscale_params['service_region'] = 'us-south'
        aiopenscale_params['key_name'] = 'aiopenscale-fastpath-instance-credentials'
        aiopenscale_params['key_role'] = 'Editor'
        generated_aios_credentials = self._getCredentials(
            aiopenscale_params, True)
        aios_credentials = {}
        if self.args.env[:3].lower() == 'icp':
            aios_credentials['data_mart_id'] = uuid.uuid4()
            aios_credentials['url'] = self.environment['aios_url']
        else:
            aios_credentials['data_mart_id'] = generated_aios_credentials['source_crn'].split(':')[7]
            aios_credentials['apikey'] = self.args.apikey
            aios_credentials['url'] = self.environment['aios_url']
        return aios_credentials

    def setupWML(self):
        wml_params = {}
        wml_params['service_display_name'] = 'Watson Machine Learning'
        wml_params['service_name'] = 'pm-20'
        wml_params['instance_name'] = 'wml-fastpath-instance'
        wml_params['service_plan_name'] = 'lite'
        wml_params['service_region'] = 'us-south'
        wml_params['key_name'] = 'wml-fastpath-instance-credentials'
        wml_params['key_role'] = 'Administrator'
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

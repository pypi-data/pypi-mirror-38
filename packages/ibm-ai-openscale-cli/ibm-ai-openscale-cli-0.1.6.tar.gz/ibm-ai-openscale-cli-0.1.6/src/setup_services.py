# coding=utf-8
from src.utils import *

class SetupIBMCloudServices(object):

    def __init__(self, args, environment):
        self.environment = environment
        self.args = args

    def _read_credentials_from_file(self, credentials_file):
        print('\t - Credentials file specified')
        print('\t - Using credentials from "{}"'.format(credentials_file))
        return jsonFileToDict(credentials_file)

    def _aios_credentials(self, data_mart_id):
        aios_credentials = {}
        aios_credentials['apikey'] = self.args.apikey
        aios_credentials['url'] = self.environment['aios_url']
        aios_credentials['data_mart_id'] = data_mart_id
        return aios_credentials

    def _aios_icp_credentials(self):
        print('Setting up {} instance'.format('AI OpenScale'))
        aios_icp_credentials = {}
        aios_icp_credentials['username'] = self.args.username
        aios_icp_credentials['password'] = self.args.password
        aios_icp_credentials['data_mart_id'] = '00000000-0000-0000-0000-000000000000'
        aios_icp_credentials['url'] = 'icp:{}'.format(self.args.url)
        return aios_icp_credentials

    def setup_postgres_database(self):
        print('Setting up {} instance'.format('Compose for PostgreSQL'))
        if self.args.postgres is not None:
            return self._read_credentials_from_file(self.args.postgres)
        print('Setting up AIOS internal database')
        return None

    def setup_aios(self):
        raise NotImplementedError

    def setup_wml(self):
        raise NotImplementedError
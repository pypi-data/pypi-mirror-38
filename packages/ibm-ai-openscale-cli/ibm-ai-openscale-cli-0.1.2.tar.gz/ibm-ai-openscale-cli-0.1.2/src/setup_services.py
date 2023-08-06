# coding=utf-8

class SetupIBMCloudServices(object):

    def __init__(self, args, environment):
        self.environment = environment
        self.args = args

    def setupAIOS(self):
        raise NotImplementedError

    def setupWML(self):
        raise NotImplementedError

    def setupPostgresDatabase(self):
        raise NotImplementedError

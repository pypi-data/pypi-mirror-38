# coding=utf-8
from __future__ import print_function

import json
import subprocess
import requests


def executeCommandWithResult(cmd):
    '''
    Run command and capture the output of the command
    '''
    status, result = subprocess.getstatusoutput(cmd)
    if status != 0:
        return None
    return result


def executeCommand(cmd):
    '''
    Run command
    '''
    status, result = subprocess.getstatusoutput(cmd)
    if status != 0:
        print('ERROR: Exited with {} status while trying to execute {}. Reason: {}'.format(status, cmd, result))
        exit(1)


def jsonFileToDict(filename):
    '''
    reads the json file specfied and returns it as a dictionary
    '''
    result = None
    if (filename is not None and filename.strip()):
        with open(filename.strip()) as f:
            result = json.load(f)
    if result is None:
        print('ERROR: Unable to read file "{}"'.format(filename))
        exit(1)
    return result


def getExplainabilityBody(modelMetaData, datamartName, serviceBinding, modelId, catagoricalColumns, aiosCredentials):
    feature_columns = [d.get('name') for d in modelMetaData['training_data_schema']
                       ['fields'] if d.get('name') != modelMetaData['label_column']]
    result = {
        'data_mart_id': aiosCredentials['data_mart_id'],
        'service_binding_id': serviceBinding,
        'model_id': modelId,
        'parameters': {
            'model_type': modelMetaData['evaluation']['method'],
            'model_data_type': 'numeric_categorical',
            'model_source': 'wml',
            'label_column': modelMetaData['label_column'],
            'feature_columns': feature_columns,
            'catagorical_columns': catagoricalColumns,
            'training_data_reference': modelMetaData['training_data_reference'][0]
        }
    }
    return result


def getIamHeaders(aiosCredentials, iam_url):
    # get a bearer token for storing historical measurementfacts
    token_data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'response_type': 'cloud_iam',
        'apikey': aiosCredentials['apikey']
    }
    response_token = requests.post(iam_url, data=token_data)
    iam_token = response_token.json()['access_token']
    iam_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % iam_token
    }
    return iam_headers

def verifyVersionOfLib(libName, minVersionTuple, howToUpgrade):
    result = executeCommandWithResult('pip show {}'.format(libName))
    for line in result.splitlines():
        if line.split()[0].strip() == 'Version:':
            version = line.split()[1].strip().split('.')
            for idx, elem in enumerate(version):
                if int(elem.strip('()')) < minVersionTuple[idx]:
                    print('Library %s must have version %s' % libName, minVersionTuple)
                    print('Please do %s' % howToUpgrade)
                    exit(1)

def get_error_message(response):
    """
    Gets the error message from a JSON response.
    :return: the error message
    :rtype: string
    """
    error_message = 'Unknown error'
    try:
        error_json = response.json()
        if 'error' in error_json:
            if isinstance(error_json['error'], dict) and 'description' in \
                    error_json['error']:
                error_message = error_json['error']['description']
            else:
                error_message = error_json['error']
        elif 'error_message' in error_json:
            error_message = error_json['error_message']
        elif 'message' in error_json:
            error_message = error_json['message']
        elif 'description' in error_json:
            error_message = error_json['description']
        elif 'errorMessage' in error_json:
            error_message = error_json['errorMessage']
        elif 'msg' in error_json:
            error_message = error_json['msg']
        return error_message
    except:
        return response.text or error_message

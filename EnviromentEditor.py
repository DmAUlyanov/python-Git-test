# -*- coding: utf-8 -*-
import re
import json
from os import listdir
from os.path import isfile, join
from Data import get_by_storeIdentificator

def get_env_files(localRepoPath):
    fastlaneDirPath = '{repoPath}/fastlane/'.format(repoPath=localRepoPath)
    files = [f for f in listdir(fastlaneDirPath) if isfile(join(fastlaneDirPath, f))]
    for file in files:
        if '.env.' in file:
            yield fastlaneDirPath + file

def save_params(filePath, paramsDic):
    result = ""
    for key in paramsDic:
        result += "{key} = {value}\n".format(key = key, value = paramsDic[key])
    file = open(filePath, 'w')
    file.write(result)
    file.close()

def edit_env_file(filePath):
    file = open(filePath, 'r')
    content = file.readlines()
    paramsDict = {
        'project_name': '',
        'app_id': '',
        'package_name': '',
        'alias': '',
        'flavor': '',
        'versionsFilePostfix': '',
        'metadata_dir': '',
        'json_key_file': '',
        'test_group_for_fabric': '',
        'CRASHLYTICS_API_TOKEN': '',
        'CRASHLYTICS_BUILD_SECRET': '',
        'locales': '"ru-RU, en-US"'
    }
    for line in content:
        if line.strip() != '':
            key, value = re.split(r' *= *', line)
            if key in paramsDict.keys():
                paramsDict[key] = value.strip('\n')
    if paramsDict['app_id'] == '':
        paramsDict['app_id'] = paramsDict['package_name']
    del paramsDict['package_name']
    paramsDict['app_id'] = paramsDict['app_id'].replace(".beta", "")
    externalData = get_by_storeIdentificator(paramsDict['app_id'].strip('"')) #в старых .env к app_id приписана .beta
    paramsDict.update(externalData)

    if paramsDict['flavor'] == '':
        del paramsDict['flavor']

    if '.beta' in filePath:
        del paramsDict['metadata_dir']
        del paramsDict['locales']
    elif '.release' in filePath:
        del paramsDict['test_group_for_fabric']
        del paramsDict['CRASHLYTICS_API_TOKEN']
        del paramsDict['CRASHLYTICS_BUILD_SECRET']
        if 'flavor' in paramsDict.keys():
            paramsDict['metadata_dir'] = '"metadata.{0}"'.format(paramsDict['flavor'].strip('"'))
        else:
            paramsDict['metadata_dir'] = '"metadata"'
    file.close()
    save_params(filePath, paramsDict)

def edit(localRepoPath):
    for filePath in get_env_files(localRepoPath):
        edit_env_file(filePath)

# main('repoes/geo4me')

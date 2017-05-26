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
        'alias': '',
        'flavor': '',
        'app_id': '',
        'package_name': '',
        'versionsFilePostfix': '',
        'metadata_dir': '',
        'json_key_file': '',
        'test_group_for_fabric': '',
        'CRASHLYTICS_API_TOKEN': '',
        'CRASHLYTICS_BUILD_SECRET': ''
    }
    for line in content:
        key, value = re.split(r' *= *', line)
        if key in paramsDict.keys():
            paramsDict[key] = value[:len(value)-1]

    externalData = get_by_storeIdentificator(paramsDict['package_name'].strip('"'))
    paramsDict.update(externalData)
    if '.beta' in filePath:
        del paramsDict['metadata_dir']
    elif '.release' in filePath:
        del paramsDict['test_group_for_fabric']
        del paramsDict['CRASHLYTICS_API_TOKEN']
        del paramsDict['CRASHLYTICS_BUILD_SECRET']
        paramsDict['metadata_dir'] = '"metadata.{0}"'.format(paramsDict['flavor'].strip('"'))
    file.close()
    save_params(filePath, paramsDict)

def edit(localRepoPath):
    for filePath in get_env_files(localRepoPath):
        edit_env_file(filePath)

# main('repoes/geo4me')
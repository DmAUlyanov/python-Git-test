import re

def read_fastfile(localRepoPath):
    curFastfile = open('{repoPath}/fastlane/Fastfile'.format(repoPath=localRepoPath), 'r')
    curFastfileText = curFastfile.read()
    curFastfile.close()
    return curFastfileText

def edit_fastfile(localRepoPath):
    curFastfileText = read_fastfile(localRepoPath)
    curBuildGradlePath = re.search(r'build_gradle_file_path = [^\n]*', curFastfileText).group()

    referenceFastfile = open('Fastfile').read()
    defaultBuildGradlePath = re.search(r'build_gradle_file_path = [^\n]*', referenceFastfile).group()
    curFastfileText = referenceFastfile.replace(defaultBuildGradlePath, curBuildGradlePath)

    curFastfile = open('{repoPath}/fastlane/Fastfile'.format(repoPath=localRepoPath), 'w')
    curFastfile.write(curFastfileText)
    curFastfile.close()
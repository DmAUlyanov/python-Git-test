import re

def read_fastlane_gradle_tasks(localRepoPath):
    curFastlaneGradleTasks = open('{repoPath}/fastlane_gradle_tasks.gradle'.format(repoPath=localRepoPath), 'r')
    curFastlaneGradleTasksText = curFastlaneGradleTasks.read()
    curFastlaneGradleTasks.close()
    return curFastlaneGradleTasksText

def edit_fastlane_gradle_tasks(localRepoPath):
    curFastlaneGradleTasksText = read_fastlane_gradle_tasks(localRepoPath)
    curGeneralMajorVersion = re.search(r'ext.generalMajorVersion = [^\n]*', curFastlaneGradleTasksText).group()
    curBuildGradlePath = re.search(r'ext.buildGradlePath = [^\n]*', curFastlaneGradleTasksText).group()

    referenceFastfile = open('fastlane_gradle_tasks.gradle').read()
    defaultGeneralMajorVersion = re.search(r'ext.generalMajorVersion = [^\n]*', curFastlaneGradleTasksText).group()
    defaultBuildGradlePath = re.search(r'ext.buildGradlePath = [^\n]*', curFastlaneGradleTasksText).group()
    curFastlaneGradleTasksText = referenceFastfile.replace(defaultGeneralMajorVersion, curGeneralMajorVersion)
    curFastlaneGradleTasksText = curFastlaneGradleTasksText.replace(defaultBuildGradlePath, curBuildGradlePath)

    curFastfile = open('{repoPath}/fastlane_gradle_tasks.gradle'.format(repoPath=localRepoPath), 'w')
    curFastfile.write(curFastlaneGradleTasksText)
    curFastfile.close()

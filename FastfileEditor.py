import re

def read_fastfile(localRepoPath):
    curFastfile = open('{repoPath}/fastlane/Fastfile'.format(repoPath=localRepoPath), 'r')
    curFastfileText = curFastfile.read()
    curFastfile.close()
    return curFastfileText
    
def edit_build_gradle(localRepoPath):
	buildGradleText = open('{repoPath}/build.gradle'.format(repoPath=localRepoPath), 'r').read()
	buildGradleText = buildGradleText.replace("apply from: 'fastlane_gradle_tasks.gradle'", "")
	buildGradleFile = open('{repoPath}/build.gradle'.format(repoPath=localRepoPath), 'w')
	buildGradleFile.write(buildGradleText)
	buildGradleFile.close()

def get_major_version_name(localRepoPath):
	fastlaneGradleTasksText = open('{repoPath}/fastlane_gradle_tasks.gradle'.format(repoPath=localRepoPath), 'r').read()
	majorVersion = re.search(r'ext.generalMajorVersion = ([^\n]*)', fastlaneGradleTasksText).group(1)
	return majorVersion
    
def remove_fastlane_gradle_tasks(localRepoPath):
	import os
	import stat
	full_path =  os.path.abspath(localRepoPath + "/fastlane_gradle_tasks.gradle").replace("\\", "/")
	print('deleting {0}'.format(full_path))
	os.chmod(full_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
	os.remove(full_path)
    
def edit_pluginfile(localRepoPath):
	print('Editing on '+ localRepoPath)
	referencePluginFileText = open('Pluginfile').read()
	curPluginFile = open('{repoPath}/fastlane/Pluginfile'.format(repoPath=localRepoPath), 'w')
	curPluginFile.write(referencePluginFileText)
	curPluginFile.close()

def edit_fastfile(localRepoPath):
    curFastfileText = read_fastfile(localRepoPath)
    curBuildGradlePath = re.search(r'build_gradle_file_path = [^\n]*', curFastfileText).group()
    
    referenceFastfile = open('Fastfile').read()
    defaultBuildGradlePath = re.search(r'build_gradle_file_path = [^\n]*', referenceFastfile).group()
    
    referenceFastfile = referenceFastfile.replace(defaultBuildGradlePath, curBuildGradlePath)
    
    majorVersion = get_major_version_name(localRepoPath)
    defaultMajorVersion = re.search(r"ENV\['general_major_version'\] = '[^\n]*'", referenceFastfile).group()
    
    referenceFastfile = referenceFastfile.replace(defaultMajorVersion, "ENV['general_major_version\'] = '" + majorVersion + "'")
    
    curFastfileText = referenceFastfile

    curFastfile = open('{repoPath}/fastlane/Fastfile'.format(repoPath=localRepoPath), 'w')
    curFastfile.write(curFastfileText)
    curFastfile.close()
    
    edit_build_gradle(localRepoPath)
    remove_fastlane_gradle_tasks(localRepoPath)
    edit_pluginfile(localRepoPath)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from git import Repo, RemoteProgress, Git
import config
import os
import stat
import FastfileEditor
import EnviromentEditor
import FastlaneGradleTasksEditor
import Data


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('update(%s, %s, %s, %s)' % (op_code, cur_count, max_count, message))


def delete_not_empty_directory(path):
    files = set(os.listdir(path))
    for file in files:
        full_path =  os.path.abspath(path + "/" + file).replace("\\", "/")
        print('deleting {0}'.format(full_path))
        if os.path.isdir(full_path):
            delete_not_empty_directory(full_path)
        else:
            os.chmod(full_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
            os.remove(full_path)

    os.rmdir(path)

def work_with_git(paths, *functions):
    for path in paths:
        localRepoPath = 'repoes/{0}'.format(path)

        #if os.path.exists(localRepoPath):
        #    delete_not_empty_directory(localRepoPath)

        #Repo.clone_from(url='https://{login}:{password}@git.geo4.pro/{path}.git'.format(login=config.user,
        #                                                                                            password=config.pwd,
        #                                                                                            path=path),
        #                    to_path=localRepoPath, branch='dev', progress=Progress())

        #for func in functions:
        #    func(localRepoPath)

        repo = Repo(localRepoPath)
        repo.git.add('.')
        repo.git.commit(m='Fastlane files modified (auto)')
        repo.git.push()




work_with_git(Data.paths, FastfileEditor.edit_fastfile)#, #FastlaneGradleTasksEditor.edit_fastlane_gradle_tasks)#, EnviromentEditor.edit, FastlaneGradleTasksEditor.edit_fastlane_gradle_tasks)

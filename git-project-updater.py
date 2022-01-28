from time import sleep
import subprocess
import json
import os

class GitProjectUpdater:
  delay = 60
  currentDir = None
  configJson = None

  def __init__(self):
    self.currentDir = os.getcwd()
    with open('./config.json') as f:
      self.configJson = json.load(f)
    if self.checkValue(self.configJson, 'sleep', [str]) and self.configJson['sleep'].isnumeric():
      self.delay = int(self.configJson['sleep'])
    elif self.checkValue(self.configJson, 'sleep', [int, float]):
      self.delay = self.configJson['sleep']

    try:
      while True:
        self.run()
        sleep(self.delay)
    except Exception as e:
      raise e

  def checkValue(self, value, key = None, types = []):
    if not value:
      return False
    if types and isinstance(types, list):
      for type in types:
        if type:
          if key:
            if isinstance(value, (dict, list)) and key in value and isinstance(value[key], type):
              return True
          elif isinstance(value, type):
            return True
      return False
    return True

  def processRepository(self, name, repo, runCommands = False):
    if (
      self.checkValue(repo, 'url', [str]) and
      self.checkValue(name, types = [str])
    ):
      print('Processing - ' + name)
      os.chdir(self.currentDir)

      if not os.path.exists(name):
        if self.checkValue(repo, 'branch', [str]):
          subprocess.run(['git', 'clone', '-b', repo['branch'], repo['url']])
        else:
          subprocess.run(['git', 'clone', repo['url']])
        runCommands = True

      os.chdir(name)
      check = subprocess.run(
        ['git', 'pull'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
      )
      pullStdout = check.stdout.decode('utf-8') if check else ''

      if pullStdout.find('up to date') == -1 and pullStdout.find('up-to-date') == -1:
        runCommands = True

      if runCommands and self.checkValue(repo, 'commands', [list]):
        for command in repo['commands']:
          if self.checkValue(command, types = [dict]):
            if self.checkValue(command, 'sleep', [str]) and command['sleep'].isnumeric():
              sleep(int(command['sleep']))
            elif self.checkValue(command, 'sleep', [int, float]):
              sleep(command['sleep'])
            if self.checkValue(command, 'command', [str]):
              os.system(command['command'])
            if self.checkValue(command, 'repository', [str]):
              self.run(command['repository'])
          elif self.checkValue(command, types = [str]):
            os.system(command)
      print('End of processing - ' + name)

  def run(self, repository: str = '') -> None:
    if self.checkValue(self.configJson, 'repositories', [dict]):
      if repository:
        if self.checkValue(self.configJson['repositories'], repository, [dict]):
          self.processRepository(repository, self.configJson['repositories'][repository], True)
      else:
        for name, repo in self.configJson['repositories'].items():
          if self.checkValue(repo, 'sleep', [str]) and repo['sleep'].isnumeric():
            sleep(int(repo['sleep']))
          elif self.checkValue(repo, 'sleep', [int, float]):
            sleep(repo['sleep'])
          self.processRepository(name, repo)


GitProjectUpdater()

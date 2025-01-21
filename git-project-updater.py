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
    with open('./git-project-updater.json') as f:
      self.configJson = json.load(f)

    if 'delay' in self.configJson and isinstance(self.configJson['delay'], int):
      self.delay = self.configJson['delay']

    try:
      while True:
        self.run()
        sleep(self.delay)
    except Exception as e:
      raise e

  def processRepository(self, name: str, repo: dict, runCommands: bool = False) -> None:
    if (
      not isinstance(repo, dict)
      or not isinstance(name, str)
      or not name
      or 'url' not in repo
      or not isinstance(repo['url'], str)
      or not repo['url']
    ):
      return None

    print('Processing: ' + name)
    os.chdir(self.currentDir)

    if not os.path.exists(name):
      subprocess.run(['git', 'clone', repo['url']])
      runCommands = True

    os.chdir(name)
    subprocess.run(['git', 'checkout', '-f', repo['branch']])
    pull = subprocess.run(['git', 'pull', '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pullStdout = pull.stdout.decode('utf-8') if pull else ''

    if pullStdout.find('file changed') != -1 or pullStdout.find('files changed') != -1:
      runCommands = True

    if runCommands and 'commands' in repo and isinstance(repo['commands'], list):
      for command in repo['commands']:
        if isinstance(command, dict):
          if 'delay' in command and isinstance(command['delay'], int) and command['delay'] > 0:
            sleep(command['delay'])
          if 'command' in command and isinstance(command['command'], str) and command['command']:
            os.system(command['command'])
          if 'repository' in command and isinstance(command['repository'], str) and command['repository']:
            self.run(command['repository'])
        elif isinstance(command, str) and command:
          os.system(command)
    print('End of processing: ' + name)

  def run(self, repository: str = '') -> None:
    if 'repositories' not in self.configJson or not isinstance(self.configJson['repositories'], dict):
      return None

    if repository and repository in self.configJson['repositories']:
      self.processRepository(repository, self.configJson['repositories'][repository], True)
    else:
      for name, repo in self.configJson['repositories'].items():
        self.processRepository(name, repo)


GitProjectUpdater()

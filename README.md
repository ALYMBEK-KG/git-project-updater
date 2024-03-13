# git-project-updater

## Project update using git

### Getting started

Run commands below to install this app:

```
git clone https://github.com/ALYMBEK-KG/git-project-updater.git
cd git-project-updater
bash install.sh
```

After installation, a `git-project-updater.json` file is created.
Add your git repos to this file, ex:

```
...
"repositories": {
  "backend": {
    "url": "https://github.com/backend.git",
    "branch": "dev",
    "commands": [
      "bash ./mvnw clean package",
      "rm /opt/tomcat/webapps/backend.war",
      "cp ./target/backend.war /opt/tomcat/webapps",
      {
        "delay": 30,
        "command": "",
        "repository": "frontend"
      }
    ]
  },
  "frontend": {
    "url": "https://github.com/frontend.git",
    "branch": "dev",
    "commands": [
      "npm ci",
      "npm run build",
      "rm -r /opt/tomcat/webapps/backend/WEB-INF/classes/static/*",
      "cp -r ./dist/* /opt/tomcat/webapps/backend/WEB-INF/classes/static"
    ]
  }
}
```

Finally restart the service and enjoy:

```
systemctl stop git-project-updater
systemctl start git-project-updater
```

P.S. Your system should have the following apps to be installed: `systemd`, `python3`

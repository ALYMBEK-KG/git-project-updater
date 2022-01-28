# git-project-updater
### Project update using git

At first clone this repository: `git clone git@github.com:ALYMBEK-KG/git-project-updater.git`\
Then enter this command: `bash git-project-updater/install.sh`\
Finally enjoy with the git-project-updater.

P.S. If your projects are private so then specify url in `config.json` to ssh connection type.\
Then generate ssh-key and add it to the ssh-agent like below:
- Generating a new key: `ssh-keygen -t ed25519 -C "your_email@example.com"` or `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
- Starting the ssh-agent: `eval "$(ssh-agent -s)"`
- Adding the new key to the ssh-agent: `ssh-add ~/.ssh/id_ed25519`
- Finally add the generated key to your git server.

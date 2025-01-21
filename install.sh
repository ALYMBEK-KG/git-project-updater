#!/bin/bash
scriptPath="$(dirname $(readlink -f $0))"
scriptPathBasename="$(basename $scriptPath)"
echo "Installing $scriptPathBasename..."

echo "[Service]
Type=simple
User=$USER
Restart=always
RestartSec=60
WorkingDirectory=$scriptPath
ExecStart=/usr/bin/python3 -u $scriptPathBasename.py

[Install]
WantedBy=multi-user.target" >"$scriptPath/$scriptPathBasename.service"

echo "{
  \"app\": \"GitProjectUpdater\",
  \"version\": 1.0,
  \"delay\": 60,
  \"repositories\": {
  }
}" >"$scriptPath/$scriptPathBasename.json"

sudo chmod -R +rx $scriptPath

if sudo systemctl list-unit-files --type service | grep $scriptPathBasename; then
  sudo systemctl disable $scriptPathBasename
fi

sudo systemctl enable "$scriptPath/$scriptPathBasename.service"
sudo systemctl start $scriptPathBasename

echo "All done!"
exit 0

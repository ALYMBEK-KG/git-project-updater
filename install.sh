#!/bin/bash
scriptPath="$(dirname $(readlink -f $0))";
scriptPathBasename="$(basename $scriptPath)";
echo "Installing $scriptPathBasename...";

echo "
[Service]
Type=simple
User=root
Group=root
Restart=always
RestartSec=60
WorkingDirectory=$scriptPath
ExecStart=/usr/bin/python3 $scriptPathBasename.py
[Install]
WantedBy=multi-user.target
" > "$scriptPath/$scriptPathBasename.service"

sudo chmod -R +rx $scriptPath;

if sudo systemctl list-unit-files --type service | grep $scriptPathBasename;
then sudo systemctl disable $scriptPathBasename;
fi;

sudo systemctl enable "$scriptPath/$scriptPathBasename.service";
sudo systemctl start $scriptPathBasename;

echo "All done!";
exit 0;

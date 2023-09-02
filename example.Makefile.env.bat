@echo off
set GH_USER=user
set GH_TOKEN=xxxx
echo %GH_TOKEN% | docker login docker.pkg.github.com -u %GH_USER% --password-stdin

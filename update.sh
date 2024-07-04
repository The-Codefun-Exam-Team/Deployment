#!/bin/sh
set -e

cd ~/Deployment

git pull
podman compose pull
podman compose down
podman compose up -d

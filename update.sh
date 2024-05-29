#!/bin/sh
set -e

cd ~/Deployment
git pull
podman compose up -d

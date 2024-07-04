#!/bin/sh
set -e

git pull
podman compose pull
podman compose down
podman compose up -d

#!/bin/sh
set -e

git pull
docker compose pull
docker compose up -d


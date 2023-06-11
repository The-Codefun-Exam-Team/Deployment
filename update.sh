#!/bin/bash
cd ~/Deployment; git pull; docker-compose up -d --pull always

# Copy this to ~/update.sh

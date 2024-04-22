#!/bin/sh
cd ~/Deployment && git pull && docker compose pull && docker compose up -d

# Copy this to ~/update.sh

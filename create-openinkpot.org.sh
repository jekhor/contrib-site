#!/bin/bash
# generates openinkpot.org site
HYDE_DIR="./oi-hyde"
SITE_DIR="./openinkpot.org"
#DEPLOY_DIR="/var/www/openinkpot.org"
DEPLOY_DIR="/home/jenner/oi/oi-deploy"
python "$HYDE_DIR/hyde.py" -g -s "$SITE_DIR" -d "$DEPLOY_DIR"

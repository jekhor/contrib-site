#!/bin/bash
# generates openinkpot.org site
HYDE_DIR="./hyde"
SITE_DIR="./openinkpot.org"
DEPLOY_DIR="/var/www/openinkpot.org"
python "$HYDE_DIR" -g -s "$SITE_DIR" -d "$DEPLOY_DIR"

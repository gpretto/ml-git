#!/bin/bash

################################################################################
# © Copyright 2020 HP Development Company, L.P.
# SPDX-License-Identifier: GPL-2.0-only
################################################################################

set -e

if ! pgrep -x "minio" >/dev/null
then
    .././minio server /data &
    ml-git clone /local_ml_git_config_server.git
    ml-git dataset show mnist
    ml-git dataset tag list mnist
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
fi

cd ../api_scripts
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root &
echo ""
cd ../workspace

/bin/sh
exec "$@"
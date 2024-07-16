#!/bin/bash

source /home/wilton/miniconda3/etc/profile.d/conda.sh

conda activate tars_env

cd /home/wilton/web

uvicorn main:app --host 0.0.0.0 --port 8000 
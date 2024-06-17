source ~/miniforge3/etc/profile.d/conda.sh
conda activate tars_env
WORKSPACE=`pwd`
export PYTHONPATH=$WORKSPACE/api:$WORKSPACE/integration/odoo:$WORKSPACE/integration/whatsapp:$WORKSPACE/samantha/src
uvicorn api.main:app --host 0.0.0.0 --port 9091
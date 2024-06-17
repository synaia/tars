source ~/miniforge3/etc/profile.d/conda.sh
conda activate tars_env
WORKSPACE=`pwd`
export PYTHONPATH=$WORKSPACE/api:$WORKSPACE/integration/odoo:$WORKSPACE/integration/whatsapp:$WORKSPACE/samantha/src
python api/cli_emu.py
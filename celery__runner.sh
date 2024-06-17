WORKSPACE=`pwd`
export PYTHONPATH=$WORKSPACE/api:$WORKSPACE/integration/odoo:$WORKSPACE/integration/whatsapp:$WORKSPACE/samantha/src
celery -A samantha.src.machinery.scheduler worker  --loglevel=DEBUG

# celery -A api.celery_worker.celery_app  purge -f
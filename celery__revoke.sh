WORKSPACE=`pwd`
export PYTHONPATH=$WORKSPACE/api:$WORKSPACE/integration/odoo:$WORKSPACE/integration/whatsapp:$WORKSPACE/samantha/src
echo $1
celery -A api.celery_worker.celery_app control revoke $1

# celery -A api.celery_worker.celery_app  purge -f
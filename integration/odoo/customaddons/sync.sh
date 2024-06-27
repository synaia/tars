source .remote_secret

echo "Procesing ${1} ${2} ..."

sshpass -p "$elmer_pass" rsync -avz -e ssh $2  elmer@138.197.112.92:/opt/odoo/customaddons

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92   "echo \"${elmer_pass}\" | sudo -S systemctl stop odoo"
# -i for install module
# -u for update module
if [[ "$1" == "INSTALL" ]]; then
   option="-i "
elif [[ "$1" == "UPDATE" ]]; then
   option="-u "
fi

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92  "/opt/odoo/odoo-bin -c /etc/odoo.conf  -r odoo -w odoo --db_host 127.0.0.1 -d synaia --stop-after-init ${option} ${2}"

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92  "echo \"${elmer_pass}\" | sudo -S systemctl start odoo"




source .remote_secret

sshpass -p "$elmer_pass" rsync -avz -e ssh $1  elmer@138.197.112.92:/opt/odoo/customaddons

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92   "echo \"${elmer_pass}\" | sudo -S systemctl stop odoo"

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92  "/opt/odoo/odoo-bin -r odoo -w odoo --db_host 127.0.0.1 -d synaia --stop-after-init  -u ${1}"

sshpass -p "$elmer_pass"  ssh elmer@138.197.112.92  "echo \"${elmer_pass}\" | sudo -S systemctl start odoo"




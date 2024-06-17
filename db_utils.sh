echo "Stoping Odoo..."
sudo systemctl stop odoo.service
echo "Wait for 10 segs.."
sleep 10
echo $1
psql -v -d synaia --host=localhost --port=5432 --username=odoo -c "DROP DATABASE synaia"
psql -v -d synaia --host=localhost --port=5432 --username=odoo < $1
sleep 10
sudo systemctl start odoo.service
sleep 5
sudo systemctl status odoo.service
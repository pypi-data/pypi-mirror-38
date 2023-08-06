#!/bin/sh

# Use this script to create a tar ball of debug information for the csr_azure_ha package
ha_status="/home/guestshell/azure/ha_status.log"
tar_file="/home/guestshell/azure/HA/ha_debug.tar"

# Write the status of each of the daemon processes running under guestshell
echo "Write the status of each process running under systemd" > $ha_status
systemctl status waagent.service >> $ha_status
systemctl status auth-token.service >> $ha_status
systemctl status atd >> $ha_status
ls /etc/systemd/system/azuremsixtn.service >> $ha_status
systemctl status azuremsixtn >> $ha_status
systemctl status azure-ha.service >> $ha_status
echo "------------" >> $ha_status
echo "Show the cron jobs" >> $ha_status
crontab -l >> $ha_status
echo "------------" >> $ha_status
echo "Show the install python packages" >> $ha_status
pip freeze >> $ha_status
echo "------------" >> $ha_status
echo "Show the files under /var/log/azure" >> $ha_status
sudo ls /var/log/azure >> $ha_status
echo "------------" >> $ha_status
echo "Dump the /var/log/messages file" >> $ha_status
sudo cat /var/log/messages >> $ha_status
echo "------------" >> $ha_status

# Gather all the log files together in a tar ball
cd /home/guestshell/azure
tar -c /var/log/waagent.log ./tools/install.log ./waagent/install.log ./HA/install.log > $tar_file

if [ -e ./tools/MetadataMgr/metadata.json ]; then
    tar --append --file=$tar_file ./tools/MetadataMgr/metadata.json
else
    echo "Metadata file not found" >> $ha_status
fi

if [ -e ./tools/TokenMgr/tokenMgr.log ]; then
    tar --append --file=$tar_file ./tools/TokenMgr/tokenMgr.log
else
    echo "tokenMgr.log file not found" >> $ha_status
fi

if [ -e ./tools/TokenMgr/token_get_rsp ]; then
    tar --append --file=$tar_file ./tools/TokenMgr/token_get_rsp
else
    echo "No token response file" >> $ha_status
fi

if [ -e /bootflash/cvac.log ]; then
    tar --append --file=$tar_file /bootflash/cvac.log
else
    echo "cvac.log file not found" >> $ha_status
fi

if [ -e ./HA/node_file ]; then
    tar --append --file=$tar_file ./HA/node_file
else
    echo "node_file file not found" >> $ha_status
fi

if [ -e ./HA/azha.log ]; then
    tar --append --file=$tar_file ./HA/azha.log
else
    echo "azha.log file not found" >> $ha_status
fi

if [ -e ./HA/events ]; then
    tar --append --file=$tar_file ./HA/events/*
else
    echo "events directory not found" >> $ha_status
fi

tar --append --file=$tar_file ./ha_status.log


# Compress the file
cd ./HA
gzip $tar_file

# Move the file to /bootflash so it can be copied off the router
mv ha_debug.tar.gz /bootflash

# Clean up
rm $ha_status
#!bin/bash

cd /home/ubuntu/meatballcraft
sudo screen -d -m sudo bash backup.sh

sudo screen -dmS server sudo bash ServerStart.sh

while true; do
  if ! sudo screen -list | grep -q "server";
    then
      currentdir=$(pwd)
      instaceid=$(curl http://169.254.169.254/latest/meta-data/instance-id)
      sudo aws s3 sync $currentdir s3://meatball-craft/server/

  echo "TERMINATING EC2 IN 2 MINUTES"
  sleep 120
  sudo aws ec2 terminate-instances --instance-ids $instaceid

    else
      sleep 10
  fi

done


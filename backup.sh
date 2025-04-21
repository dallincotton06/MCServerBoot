cd ~/Server
currentdir=$(pwd)

while true; do
  if [ -z $(curl -Is http://169.254.169.254/latest/meta-data/spot/termination-time | head -1 | grep 404 | cut -d ' ' -f 2) ]; then
    sudo aws s3 sync $currentdir s3://your-s3-bucket #UPDATE
      break
        else
          sleep 5
        fi
done


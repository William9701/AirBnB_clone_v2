#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

sudo apt update
sudo apt-get -y upgrade
# Install Nginx if it not already installed
if ! dpkg -l | grep -q "nginx"; then
    sudo apt-get -y install nginx
fi

# Create the folder /data/ if it doesn’t already exist
if [ ! -d "/data/" ]; then
    sudo mkdir "/data/"
fi

# Create the folder /data/web_static/ if it doesn’t already exist
if [ ! -d "/data/web_static/" ]; then
    sudo mkdir "/data/web_static/"
fi

# Create the folder /data/web_static/releases/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/" ]; then
    sudo mkdir "/data/web_static/releases/"
fi

# Create the folder /data/web_static/shared/ if it doesn’t already exist
if [ ! -d "/data/web_static/shared/" ]; then
    sudo mkdir "/data/web_static/shared/"
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/test/" ]; then
    sudo mkdir "/data/web_static/releases/test/"
fi

# Create a fake HTML file
if [ ! -e "/data/web_static/releases/test/index.html" ]; then
    cat <<EOF > "/data/web_static/releases/test/index.html"
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF
fi

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
if [ -L "/data/web_static/current" ]; then
  rm -rf "/data/web_static/current"
fi
sudo ln -s "/data/web_static/releases/test/" "/data/web_static/current"

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data

# Path to Nginx site configuration file
nginx_config_file="/etc/nginx/sites-available/default"

if [ ! -f "$nginx_config_file" ]; then
    exit 1
fi

# Check if the 'location' block for /hbnb_static/ already exists
if ! grep -q "location /hbnb_static/ {" "$nginx_config_file"; then
    sudo sed -i '/^server {/a \
        location /hbnb_static/ {\
            alias /data/web_static/current/;\
        }' "$nginx_config_file"
fi

# Restart Nginx
sudo service nginx restart
#!/bin/bash

# Stop and remove existing containers
docker-compose down

# Rebuild the containers
docker-compose build --no-cache

# Start the containers
docker-compose up -d

# Verify nginx configuration
docker exec lernassistent_nginx nginx -t

# Check file permissions and existence
docker exec lernassistent_nginx ls -la /usr/share/nginx/html/View/

# Test CSS file headers
echo "Testing CSS file headers..."
curl -I http://maguna.me/View/Styles.css
curl -I http://maguna.me/View/DashboardStyles.css

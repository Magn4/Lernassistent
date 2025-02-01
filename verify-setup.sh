#!/bin/bash

echo "=== Checking nginx configuration ==="
docker exec nginx nginx -t

echo -e "\n=== Listing files in View directory ==="
docker exec nginx ls -la /usr/share/nginx/html/View/

echo -e "\n=== Testing CSS file access ==="
for css in Styles.css NavigationStyles.css DashboardStyles.css; do
    echo -e "\nTesting /View/$css:"
    curl -I "http://127.0.0.1/View/$css"
done

echo -e "\n=== Checking nginx error log ==="
docker exec nginx tail -n 20 /var/log/nginx/error.log

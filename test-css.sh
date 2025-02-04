
#!/bin/bash

echo "Testing CSS file access..."
curl -I http://127.0.0.1/View/Styles.css
curl -I http://127.0.0.1/View/DashboardStyles.css
curl -I http://127.0.0.1/View/NavigationStyles.css

echo -e "\nChecking directory contents..."
docker exec lernassistent_nginx ls -la /usr/share/nginx/html/View/
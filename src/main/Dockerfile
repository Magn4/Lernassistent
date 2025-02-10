# Use the official Nginx image
FROM nginx:latest

# Copy your custom Nginx configuration file into the container
# Make sure nginx.conf is present in the same directory as this Dockerfile
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally, you can copy static content (e.g., a website's HTML files) to the Nginx server
COPY ./View /usr/share/nginx/html

# Expose the HTTP port (default is 80)
EXPOSE 80

# Set permissions to ensure Nginx can access the config file (if needed)
# RUN chown -R nginx:nginx /etc/nginx/nginx.conf

# Start Nginx and keep it running in the foreground
CMD ["nginx", "-g", "daemon off;"]

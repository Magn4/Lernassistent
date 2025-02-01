FROM nginx:alpine

# Install necessary tools
RUN apk add --no-cache bash

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory structure
RUN mkdir -p /usr/share/nginx/html/View/assets

# Copy files with explicit paths
COPY src/main/View/*.html /usr/share/nginx/html/View/
COPY src/main/View/*.css /usr/share/nginx/html/View/
COPY src/main/View/assets /usr/share/nginx/html/View/assets/

# Set proper permissions and ownership
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    find /usr/share/nginx/html -type f -name "*.css" -exec chmod 644 {} \;

# Verify file existence and permissions (during build)
RUN ls -la /usr/share/nginx/html/View/

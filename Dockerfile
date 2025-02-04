FROM nginx:alpine

# Install necessary tools
RUN apk add --no-cache bash

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory structure
RUN mkdir -p /usr/share/nginx/html/View
RUN mdkir -p /usr/share/nginx/html/View/View

# Copy files with explicit paths
COPY src/main/View/*.html /usr/share/nginx/html/View/
COPY src/main/View/*.css /usr/share/nginx/html/View/View/

# Debug: List files and fix permissions
RUN echo "Listing View directory contents:" && \
    ls -la /usr/share/nginx/html/View/ && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    find /usr/share/nginx/html -type f -name "*.css" -exec chmod 644 {} \; && \
    echo "File permissions updated"

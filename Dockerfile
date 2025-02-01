FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy HTML and asset files
COPY src/main/View/*.html /usr/share/nginx/html/View/
COPY src/main/View/*.css /usr/share/nginx/html/View/
COPY src/main/View/assets /usr/share/nginx/html/View/assets

# Create required directories
RUN mkdir -p /usr/share/nginx/html/View

# Set permissions
RUN chmod -R 755 /usr/share/nginx/html

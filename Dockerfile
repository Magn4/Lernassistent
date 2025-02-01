FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create the View directory
RUN mkdir -p /usr/share/nginx/html/View

# Copy HTML and CSS files to the View directory
COPY src/main/View/*.html /usr/share/nginx/html/View/
COPY src/main/View/*.css /usr/share/nginx/html/View/
COPY src/main/View/assets /usr/share/nginx/html/View/assets

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html

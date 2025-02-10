# Use the official Caddy image
FROM caddy:latest

# Copy your custom Caddy configuration file into the container
COPY Caddyfile /etc/caddy/Caddyfile

# Optionally, you can copy static content (e.g., a website's HTML files) to the Caddy server
COPY ./View /usr/share/caddy

# Expose the HTTP and HTTPS ports
EXPOSE 80
EXPOSE 443

# Start Caddy and keep it running in the foreground
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]

# Multi-stage build for React app
FROM node:18-alpine as build

# Set working directory
WORKDIR /web_app

# Copy package files first for better layer caching
COPY web_app/package*.json ./

RUN npm install

# Copy the rest of the app source code
COPY web_app .

# Build the app
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Copy built app to nginx html directory
COPY --from=build /web_app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
# Use node as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose the port Vite uses for dev mode
EXPOSE 5173

# Default command to start the React app
CMD ["npm", "run", "dev"]

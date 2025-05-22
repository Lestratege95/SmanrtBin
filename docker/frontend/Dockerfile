FROM node:16-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Install serve to run the app
RUN npm install -g serve

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"] 
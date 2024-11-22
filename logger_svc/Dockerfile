# Use an official Node.js runtime as a parent image
FROM node:22

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Ensure the .env file is copied
COPY .env.prod .env
# Expose the port the app runs on
EXPOSE 82

# Define the command to run the application
CMD ["node", "server.js"]

# docker build -t naphat58021/weather_logger .
# docker run -d -p 82:82 --name logger_svc -it naphat58021/weather_logger
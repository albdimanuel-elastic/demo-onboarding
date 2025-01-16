FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Ensure the /var/log directory exists with proper permissions
RUN mkdir -p /var/log && chmod -R 777 /var/log

EXPOSE 3000

CMD ["node", "app.js"]
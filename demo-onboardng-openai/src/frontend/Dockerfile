FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Create the /var/log directory
RUN mkdir -p /var/log

EXPOSE 3000

CMD ["node", "app.js"]
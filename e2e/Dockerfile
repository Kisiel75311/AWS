FROM node:alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci \
 && rm -rf node_modules \
 && rm package-lock.json

COPY . .

RUN npm i

CMD ["npm", "run", "dev"]

FROM node:18-alpine

WORKDIR /app

# копируем только package.json
COPY package.json ./
RUN npm install

# копируем весь остальной проект
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]

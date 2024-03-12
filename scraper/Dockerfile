FROM node:20.11-alpine3.18

WORKDIR /scraper

ENV NODE_ENV=production

COPY package*.json ./

RUN NODE_ENV=development npm ci --ignore-scripts --audit=false --fund=false

COPY . .

RUN npm run build

USER node

CMD ["node", "dist/index.js"]
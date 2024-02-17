FROM node:20.11-alpine3.18

WORKDIR /scraper

COPY package*.json .

RUN npm ci --ignore-scripts --audit=false --fund=false

COPY . .

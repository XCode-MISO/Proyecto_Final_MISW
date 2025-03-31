# syntax=docker/dockerfile:1.4

FROM node:22-slim as builder

RUN mkdir /project
WORKDIR /project


COPY package.json package-lock.json ./
RUN npm ci
RUN npm run build

COPY . .

CMD ["ng", "serve", "--host", "0.0.0.0"]
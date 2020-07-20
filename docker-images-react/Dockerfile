FROM node:14-stretch-slim AS base
WORKDIR /usr/src/app

COPY package.json yarn.lock ./
RUN yarn install

ENTRYPOINT [ "yarn", "start" ]
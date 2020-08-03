FROM node:14-stretch-slim AS base
WORKDIR /usr/src/app

FROM base AS dev
COPY package.json yarn.lock ./
RUN yarn install
ENTRYPOINT [ "yarn", "start" ]

# リクエスト先のAPIサーバーを別立てにしなければいけないため参考実装
# （developではpackage.jsonの記述によってProxyされるが、ビルドするとJSとCSSのみで動くため）
FROM base AS prod
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY . .
RUN yarn install
RUN yarn add serve -g
ENTRYPOINT [ "yarn", "prod" ]
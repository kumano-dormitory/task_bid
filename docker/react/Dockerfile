FROM node:lts-alpine3.16
WORKDIR /usr/src/react
RUN npm install yarn
COPY ./react .
RUN yarn install
WORKDIR /usr/src/scripts
COPY ./scripts .
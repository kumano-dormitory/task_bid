FROM node:lts-alpine3.16
WORKDIR /usr/src/react
RUN npm install yarn
ADD ./react .
RUN yarn install
WORKDIR /usr/src/scripts
COPY ./scripts .
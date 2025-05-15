FROM ubuntu:latest
LABEL authors="xxx64"
FROM node:22.15.0 as build

COPY package.json package.json
RUN npm install
COPY . .
RUN npm build

FROM nginx:1.24.0
COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD["nginx","-g","daemon off;"]
FROM node:18-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-alpine as production-stage

RUN apk add --no-cache gettext

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY nginx.conf.template /etc/nginx/conf.d/nginx.conf.template
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
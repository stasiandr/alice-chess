FROM nginx:1.17-alpine
ADD /etc/letsencrypt/live/stas.dtransform.online /var/www/cert
RUN rm /etc/nginx/conf.d/default.conf 
COPY nginx.conf /etc/nginx/conf.d
FROM nginx:1.17-alpine
ADD /etc/letsencrypt/live/stas.dtransform.online 
RUN rm /etc/nginx/conf.d/default.conf /var/www/cert
COPY nginx.conf /etc/nginx/conf.d
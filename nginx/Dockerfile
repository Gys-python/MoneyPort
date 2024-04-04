FROM nginx:latest

# Копируйте ваш конфигурационный файл в контейнер
COPY ./default.conf /etc/nginx/conf.d/

# Откройте порт 80 для входящих соединений
EXPOSE 80

# Запустите Nginx в фоновом режиме
CMD ["nginx", "-g", "daemon off;"]

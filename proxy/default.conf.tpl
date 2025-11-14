server {
    listen 80;
    server_name faxriddinbek.uz 64.226.100.202;

    location /static/ {
        alias /vol/web/static/;
    }

    location /media/ {
        alias /vol/web/media/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass app:9000;
    }
}
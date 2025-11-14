server {
    listen 80;
    server_name ezma.uz www.ezma.uz 159.89.101.198;

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
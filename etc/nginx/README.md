# NGINX PLUS


## MONITORING DASBOARD


Add to `/etc/nginx/conf.d/default.conf`:

```conf
# /etc/nginx/conf.d/default.conf

# enable /api/ location with appropriate access control in order
# to make use of NGINX Plus API
location /api/ {

    limit_except GET {
        auth_basic "NGINX Plus API";

        # With OpenSSL 1.1.1:
        #   echo -n "${USER}:" > .passwd.hash && openssl passwd -6 >> /etc/nginx/.passwd.hash
        #   cat /etc/nginx/.passwd.hash
        auth_basic_user_file /etc/nginx/.passwd.hash;
    }

   api write=on;
   #allow 127.0.0.1;
   #deny all;
}

# enable NGINX Plus Dashboard; requires /api/ location to be
# enabled and appropriate access control for remote access
location = /dashboard.html {
   root /usr/share/nginx/html;
}
```

# APPROOV NGINX CONFIGURATION

## APPROOV REQUIREMENTS

### Lua Programming Language

The Approov module for Nginx Plus requires [Lua](https://www.lua.org/start.html), and its package manager [LuaRocks](https://github.com/luarocks/luarocks/wiki/Installation-instructions-for-Unix).

Installing Lua and LuaRocks:

```
./bin/install-lua
```

and after a very long output we should be able to see the installed versions for Lua and LuaRocks:

```
--------------------- VERSIONS ---------------------

Lua 5.1.4  Copyright (C) 1994-2008 Lua.org, PUC-Rio

/usr/local/bin/luarocks 3.2.1
LuaRocks main command-line interface

----------------------------------------------------
```

### Install the Approov Module for Nginx Plus

To only install the Approov module for Nginx Plus:

```
./bin/install-approov
```

To also copy the server examples, that will not override any existing file in `/etc/nginx/conf.d`:

```
./bin/install-approov --with-server-examples
```

If it his a brand new and not yet customized Nginx installation, a quick start would be:

```
./bin/install-approov --with-nginx-conf --with-server-examples
```

> **NOTE:** The old `/etc/nginx/nginx.conf` will be preserved as a backup file.


## NGINX MAIN CONFIGURATION

Edit `/etc/nginx/nginx.conf` in your favorite editor.

After this:

```nginx
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;
```

include the necessary dependencies:

```nginx
include /etc/nginx/modules/approov/dependencies.conf;
```

The full file can be seen [here](/etc/nginx/nginx.conf).

### Testing the Nginx configuration

Run the test for syntax errors with:

```
$ nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Reload the configuration to test that its able to include the Lua modules:

```
nginx -s reload
```

Visit again the server url, like http://localhost:8002, and confirm that the Nginx `index.html` page is still working.


## APPROOV NGINX SERVER CONFIGURATION

For this example we have a very simple [backend server](/backend), and we will root the traffic to it by using Nginx Plus with Approov to protect some of the API endpoints.

By looking into the full [approov-example.conf](/etc/nginx/conf.d/approov-example.conf) file we can observe that we need to require the Approov module and then include a specific Approov Lua file in each API endpoint we want to protect with Approov.

We require the Approov module with:

```nginx
lua_package_path "/etc/nginx/modules/?.lua;;/etc/nginx/modules/approov/?.lua;;";
```

To protect an API endpoint with an Approov Token its necessary to include inside each location block:

```nginx
# Changes the default header from `Authorization` to `Approov-Token`
auth_jwt   "APPROOV" token=$http_Approov_Token;

# Relative path to the `nginx.conf` for the file `approov-secret.jwk`, that contains the Approov base64url encoded secret to be used to verify the Approov Tokens signature.
```

or if we want the additional protection for checking the Approov Token and for the Approov Token binding, then we include inside each location block:

```nginx
auth_jwt          "APPROOV" token=$http_Approov_Token;
auth_jwt_key_file approov-secret.jwk;

access_by_lua '
    local approov = require("token-binding-check")
    approov.checkTokenBinding(ngx.var.jwt_claim_pay, ngx.var.http_Authorization)
';
```

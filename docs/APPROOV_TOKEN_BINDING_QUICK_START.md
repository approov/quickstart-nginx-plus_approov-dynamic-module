# APPROOV TOKEN BINDING QUICK START

This quick start is for developers familiar with NGINX Plus who are looking for a quick intro into how they can add [Approov](https://approov.io) into an existing project. Therefore this will guide you through the necessary steps for adding Approov to an existing NGINX Plus instance.

We strongly advise you to try first this quick start in a development environment, and just follow it in a production environment when you understand how Approov works within your NGINX Plus deployment.

## APPROOV REPOSITORY

Clone the Approov repository from Github:

```
git clone https://github.com/approov/nginx-plus_approov-dynamic-module.git
```

Now switch to inside the repo:

```
cd nginx-plus_approov-dynamic-module
```

## APPROOV TOKEN BINDING WITH NGINX PLUS DYNAMIC MODULE

### Lua Programming Language

The Approov module for NGINX Plus requires [Lua](https://www.lua.org/start.html), and its package manager [LuaRocks](https://github.com/luarocks/luarocks/wiki/Installation-instructions-for-Unix).

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

### Install the Approov Module for NGINX Plus

To only install the Approov module for NGINX Plus:

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

## APPROOV CLI TOOL

If you haven't done it already, please follow [these instructions](https://approov.io/docs/latest/approov-installation/#approov-tool) from the Approov docs to download and install the [Approov CLI Tool](https://approov.io/docs/latest/approov-cli-tool-reference/).

Don't forget to export your Approov management token:

```
export APPROOV_MANAGEMENT_TOKEN=$(cat /path/to/development.token)
```

> **NOTE:**
>
> The above export is only valid for the current shell session. 
> If you open another shell you need to repeat it. 
> Add it to your `.bashrc` file in order to persist it across shell sessions.


## APPROOV API

Approov needs to know the domain name for the API its authorized to issue valid tokens.

Add it with:

```
approov api -add your.api.domain.com
```

Now that Approov knows the domain for your API you get [dynamic certificate pinning](https://approov.io/docs/latest/approov-usage-documentation/#approov-dynamic-pinning) out of the box for free.


## APPROOV SECRET

We need an [Approov secret](https://approov.io/docs/latest/approov-cli-tool-reference/#secret-command) to check the signature in the JWT tokens and we need to use the same one used by the [Approov Cloud service](https://www.approov.io/approov-in-detail.html) to sign the [Approov Tokens](https://www.approov.io/docs/latest/approov-usage-documentation/#approov-tokens) issued to our mobile app.

### Retrieve the Approov Secret

```
approov secret /path/to/approov/administration.token -get base64url
```

### Set the Approov Secret Unique Key Identifier(KID)


The `kid` identifier must be presented in the JWT header of any Approov Token we want to verify, otherwise Nginx will not know what secret to use to verify it, and the validation will fail.

So set it in the Approov cloud service with this command:

```
 approov secret /path/to/approov//administration.tok -setKeyID 0001
```

Now the Approov cloud service will always add the `kid` you set to any Approov Token it issues.

Approov Token header example:

```json
{
  "typ": "JWT",
  "alg": "HS256",
  "kid": "0001"
}
```

> **NOTE:** 
>
> To bear in mind that the `kid` can have a more complex unique identifier, than the `0001` used here, and *MUST* be unique in the `*.jwk` file where you will save it in the next step. 


## NGINX PLUS CONFIGURATION

### Add the Approov Secret to the NGINX PLus key File 

In the same folder where `/etc/nginx/nginx.conf` is located create the file `approov-secret.jwk` and add to it:

```json
{"keys":
    [{
        "k":"APPROOV_BASE64URL_SECRET_HERE",
        "kty":"oct",
        "kid":"APPROOV_SECRET_UNIQUE_KEY_IDENTIFIER_HERE"
    }]
}
```

Don't forget to replace `APPROOV_BASE64URL_SECRET_HERE` and `APPROOV_SECRET_UNIQUE_KEY_IDENTIFIER_HERE` with their correct values. Afterwards, the file should look similar to this:

```json
{"keys":
    [{
        "k":"NTQ0ZDVkZWE4ZjE0OTJjMjUxMmZiZGNjZjY2NTllNTIxNmQzZjA4MGZiMTY0ZDRhMDNkYjcwMGY2YWY1OGI3NzRiNTM3NWVhYjI2MDA3OTViYjVkOTVjYWQyM2QxNThlYWM4Y2I0OGFmOWJlMzdjMDFjY2YyYThiZjNiNzZiOWYK",
        "kty":"oct",
        "kid":"0001"
    }]
}
```

> **NOTE:** 
>
> The above values for `k` and for `kid` are just fake ones.

### Add the Check for the Approov Token Binding

For the Approov Token binding to work we need to load the Approov Token Binding dynamic module.

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

An example file can be seen [here](/etc/nginx/nginx.conf).

Now you can enable the Approov Token Binding in any API endpoint like this:

```nginx
location /api/v2 {

    # APPROOV TOKEN CHECK:
    auth_jwt   "APPROOV" token=$http_Approov_Token;
    auth_jwt_key_file approov-secret.jwk;

    # APPROOV TOKEN BINDING CHECK
    access_by_lua '
        local approov = require("token-binding-check")
        approov.checkTokenBinding(ngx.var.jwt_claim_pay, ngx.var.http_Authorization)
    ';

    # rest of your nginx configuration...
}
```

So now we have more three lines to add in order to require and invoke the Lua dynamic module that will check for the Approov Token Binding.


## TESTING THE APPROOV TOKEN BINDING CHECK IN NGINX PLUS

### Requests with an Approov Token Binding

#### Valid Approov Token Binding

This request example is for a valid Approov Token Binding, where we will bind the authorization header `AUTH_TOKEN_HERE` with the Approov Token. 

We will use the Approov CLI tool to generate an example for a valid Approov Token Binding, that for your convenience is in-lined in the `curl` command.

##### request:

```
curl -i -X GET \
  https://your.api.domain.com/api/v2 \
  -H 'Authorization: Bearer AUTH_TOKEN_HERE' \
  -H "Approov-Token: $(approov token -setDataHashInToken "Bearer AUTH_TOKEN_HERE" -genExample your.api.domain.com | head -1)"
```

##### response:

```
HTTP/1.1 200 OK
Server: nginx/1.17.6
...
```

#### Invalid Approov Token Binding  

This request example is for an invalid Approov Token Binding where the binding is missing or is not matching. 

For this example we will test the scenario where the binding is missing, therefore this time the Approov token command will not generate an Approov token with the binding for the authorization header. 

##### request:

```
curl -i -X GET \
  https://your.api.domain.com/api/v2 \
  -H 'Authorization: Bearer AUTH_TOKEN_HERE' \
  -H "Approov-Token: $(approov token -genExample your.api.domain.com | head -1)"
```

##### response:

```
HTTP/1.1 401 Unauthorized
Server: nginx/1.17.6
...
```

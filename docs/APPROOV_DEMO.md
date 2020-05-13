# APPROOV DEMO 

We recommend to follow this Approov Integration example in a Docker container for Centos, and we will provide some [bash scripts](/bin/) to help with the docker commands and all the setup needed to be up and running. More detailed information can be found in [DOCKER_STACK.md](/docs/DOCKER_STACK.md).

## THE SCOPE

We will focus on a quick start example of integrating the Approov dynamic module in a vanilla installation of the Nginx Plus server, while the [APPROOV_NGINX_CONFIGURATION.md](/docs/APPROOV_NGINX_CONFIGURATION.md) will contain more detailed information on how the Approov Token check can be integrated in a current Nginx Plus server configuration.


## APPROOV REPOSITORY

Clone the Approov repository from Github:

```
git clone https://github.com/approov/nginx-plus_approov-dynamic-module.git
```

Now switch to inside the repo:

```
cd nginx-plus_approov-dynamic-module
```

## APPROOV SECRET

The Approov secret used in this demo, that you are about to create, his not a production secret, aka, obtained via the [Approov CLI tool](https://www.approov.io/docs/v2.1/approov-cli-tool-reference/#secret-command), instead it was generated with OpenSSL.

### Generate an Approov Base64URL Encoded Secret for Test Purposes

The self generated Approov base64url encoded secret is only useful for testing purposes, like when using Curl, Postman or similar tools to issue the requests.

##### bash command:

```
openssl rand -hex 64 | base64url
```

> **NOTE**: The `base64url` command is part of the `basez` package in Linux.


##### output:

```
NTQ0ZDVkZWE4ZjE0OTJjMjUxMmZiZGNjZjY2NTllNTIxNmQzZjA4MGZiMTY0ZDRhMDNkYjcwMGY2YWY1OGI3NzRiNTM3NWVhYjI2MDA3OTViYjVkOTVjYWQyM2QxNThlYWM4Y2I0OGFmOWJlMzdjMDFjY2YyYThiZjNiNzZiOWYK
```

> **IMPORTANT:**
>
>For a production backend you will need to use the [Approov CLI tool](https://www.approov.io/docs/v2.1/approov-cli-tool-reference/#secret-command):
>
>```
>approov secret /path/to/approov/administration.token -get base64url
>```

### Set the Approov Base64URL Encoded Secret

Copy the example `.jwk` file with:

```
cp ./etc/nginx/approov-secret.jwk.example ./etc/nginx/approov-secret.jwk
```

Now edit the file `./etc/nginx/approov-secret.jwk`, and add the correct values for `APPROOV_BASE64URL_SECRET_HERE` and `APPROOV_SECRET_UNIQUE_KEY_IDENTIFIER_HERE`:


```json
{"keys":
    [{
        "k":"APPROOV_BASE64URL_SECRET_HERE",
        "kty":"oct",
        "kid":"APPROOV_SECRET_UNIQUE_KEY_IDENTIFIER_HERE"
    }]
}
```

Using the secret that we generated above, the file should look like this:

```json
{"keys":
    [{
        "k":"NTQ0ZDVkZWE4ZjE0OTJjMjUxMmZiZGNjZjY2NTllNTIxNmQzZjA4MGZiMTY0ZDRhMDNkYjcwMGY2YWY1OGI3NzRiNTM3NWVhYjI2MDA3OTViYjVkOTVjYWQyM2QxNThlYWM4Y2I0OGFmOWJlMzdjMDFjY2YyYThiZjNiNzZiOWYK",
        "kty":"oct",
        "kid":"0001"
    }]
}
```

To bear in mind that the `kid` can have a more complex unique identifier, than the `0001` used here. 

The `kid` identifier must be presented in the JWT header of any Approov Token we want to verify, otherwise Nginx will not know what secret to use to verify it, and the validation will fail.

JWT header [example](https://jwt.io/#debugger-io?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjQ3MDg2ODM0NTcuNDg1Mzk1LCJwYXkiOiI1NjZ2UVdhV0dCZ3MrS0U4eXNqVFRQUXRncHVlK1hMTXF4OGVZb2JDckkwPSJ9.5tsHeglDEv_89lPVKjCmMWrfPW3phvcgDEGlNn7ZACU):

```json
{
  "typ": "JWT",
  "alg": "HS256",
  "kid": "0001"
}
```

> **NOTE**: You can use the Approov base64url encoded from this README to verify the signature for this example, that we link to jwt.io. Just replace the secret where it says `your-256-bit-secret` and tick the box for `secret base64 encoded`, and the JWT token must match with this one:
>```
>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjQ3MDg2ODM0NTcuNDg1Mzk1LCJwYXkiOiI1NjZ2UVdhV0dCZ3MrS0U4eXNqVFRQUXRncHVlK1hMTXF4OGVZb2JDckkwPSJ9.5tsHeglDEv_89lPVKjCmMWrfPW3phvcgDEGlNn7ZACU
>``` 

## CENTOS SERVER

### Nginx Plus Certificate

In order to install Nginx Plus its necessary to have the certificate and private key, and we assume that both are located at `/etc/ssl/nginx`, on the host machine.

The location can be changed with the flag `--nginx-cert-path /some/dir` when invoking the script `./bin/docker-centos [options] <command>`.

### Server Domain Certificate

This Approov Integration example will run hover HTTPS on port `8002`, and will reuse the certificate for the domain listening on the HTTPS port `443`, that is expected to be located at `/etc/letsencrypt/live`, on the host machine, but it can be changed with the flag `--domain-cert-path /some/dir` when invoking the script `./bin/docker-centos [options] <command>`.

### Build the Backend

```
./bin/docker-backend build
```

### Start the Backend

```
./bin/docker-backend up
```

> **NOTE:** This backend will be available only inside the local computer/server network.

### Running Nginx Plus with Centos 7 on a Docker Container

```
./bin/docker-centos shell
```

> **NOTE:** Unless otherwise stated, any following shell command we mention should be executed inside the docker container shell for Centos 7.


### Installing Nginx Plus, Lua and all necessary dependencies

```
./bin/install-all --with-nginx-conf --with-server-examples
```

### Starting the Nginx Plus Server in the Background

```
nginx
```

> **NOTE:** If you want to play around with the Nginx configuration you need to reload the Nginx Plus server with `./bin/nginx-reload`.

### Watching the Logs in Real Time

#### Nginx Plus logs:

```
./bin/nginx-realtime-logs
```

#### Backend logs

From a **shell in your host machine**, run:

```
docker container logs -f approov-backend
```

### Smoke Testing the API

We will use curl to quickly see an example of making a request with a valid and invalid token.

All curl commands must run from a **shell in your host machine**.

#### Valid Approov Token Header

This example is for a valid Approov Token Header that includes the token binding for the Authorization Header.

##### request:

```
curl -i -X GET \
  https://nginx-plus-demo.pdm.approov.io:8002/api/approov-token-binding-protected \
  -H 'Approov-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjQ3MTgwMTgyMjQuNzgwMzY4LCJwYXkiOiJWUUZGUEpaNjgyYU90eFJNanowa3RDSG15V2VFRWVTTXZYaDF1RDhKM3ZrPSJ9.KenfIMVdNBZPyA1RKCID5L-9YT5gZGPnz91HxxYGJb4' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Cache-Control: no-cache'
```

> **NOTE**: For demo purposes this token was signed with the same Approov base64url secret we have generated above with the `openssl` command.

##### response:

```
HTTP/1.1 200 OK
Server: nginx/1.17.6
Date: Fri, 24 Jan 2020 11:21:22 GMT
Content-Type: application/json
Content-Length: 71
Connection: keep-alive

{
  "hostname": "6c2718503db7",
  "status": "APPROOV_TOKEN_BINDING_PROTECTED"
}
```

#### Invalid Approov Token Header

This example also contains the token binding, but this time the Authorization token used in the Approov Token binding doesn't match with the one in the request.

##### request:

```
curl -i -X GET \
  https://nginx-plus-demo.pdm.approov.io:8002/api/approov-token-binding-protected \
  -H 'Approov-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjQ3MDg2ODM0NTcuNDg1Mzk1LCJwYXkiOiI1NjZ2UVdhV0dCZ3MrS0U4eXNqVFRQUXRncHVlK1hMTXF4OGVZb2JDckkwPSJ9.5tsHeglDEv_89lPVKjCmMWrfPW3phvcgDEGlNn7ZACU' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Cache-Control: no-cache'
```

##### response:

```
HTTP/1.1 401 Unauthorized
Server: nginx/1.17.6
Date: Fri, 24 Jan 2020 11:23:15 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2
Connection: keep-alive

{}
```

### API Requests with Postman

A ready to use Postman collection can be found [here](/docs/assets/postman/Approov_Nginx_Plus.postman_collection.json), that contains a very comprehensive set of example requests for valid and invalid Approov Tokens.

> **NOTE:** The collection was tailored for this Approov integration example, thus it will not work with the Approov integration in your own API backend, and requires that the file [approov-secret.jwk](./etc/nginx/approov-secret.jwk) uses the same Approov base64url secret we have generated above with the `openssl` command.


### Cleanup

When you are done with testing the Approov Integration with Nginx Plus or you just want to restart from a clean state, just completely remove it from your system:

```
./bin/uninstall
```

Basically we will stop and remove the docker container for Centos and Backend, and also the official docker images for `centos:7` and `python:3.8-slim`, plus the custom built for `approov/backend`.

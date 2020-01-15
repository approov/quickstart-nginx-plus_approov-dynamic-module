# APPROOV DYNAMIC MODULE FOR NGINX PLUS

The Approov dynamic module for Nginx Plus will show how simple is to integrate the [Approov Token](https://www.approov.io/docs/v2.1/approov-usage-documentation/#approov-tokens) check to protect the access to an API backend, without requiring any changes to its code, by leveraging the Nginx Plus support for dynamic modules in order to include the Approov Token check functionality, that only requires minimal changes to the actual Nginx Plus configuration.

If you landed in this repo without any prior knowledge about [Approov](https://approov.io/), then take a look at our overall architecture:

![Approov Architecture](/docs/assets/img/approov-overall-architecture.png)

Now if you are serious or just curious about API and Mobile App security, then we invite you to keep tabs on our [Blog](https://blog.approov.io), that its regularly updated with educational content on this topics.


## THE SCOPE

The README will focus on a quick start example of integrating the Approov dynamic module in a vanilla installation of the Nginx Plus server, while the [APPROOV_NGINX_CONFIGURATION.md](/docs/APPROOV_NGINX_CONFIGURATION.md) will contain more detailed information on how the Approov Token check can be integrated in a current Nginx Plus server configuration.


## APPROOV REPOSITORY

Clone the Approov repository from Github:

```
git clone https://github.com/approov/nginx-plus_approov-dynamic-module.git
```

Now switch to inside the repo:

```
cd nginx-plus_approov-dynamic-module
```

## QUICK START

We recommend to follow this Approov Integration example in a Docker container for Centos, and we will provide some [bash scripts](/bin/) to help with the docker commands and all the setup needed to be up and running. More detailed information can be found in [DOCKER_STACK.md](/docs/DOCKER_STACK.md).

### Nginx Plus Certificate

In order to install Nginx Plus its necessary to have the certificate and private key, and we assume that both are located at `/etc/ssl/nginx`, on the host machine.

The location can be changed with the flag `--nginx-cert-path /some/dir` when invoking the script `./bin/docker-centos [options] <command>`.

### Server Domain Certificate

This Approov Integration example will run hover HTTPS on port `8002`, and will reuse the certificate for the domain listening on the HTTPS port `443`, that is expected to be located at `/etc/letsencrypt/live`, on the host machine, but it can be changed with the flag `--domain-cert-path /some/dir` when invoking the script `./bin/docker-centos [options] <command>`.

### Environment Variables

For running this integration example you don't need to worry about them, because all it's taken care for you, but when you decide to use Approov in your API backend, then you must follow the steps in [ENVIRONMENT_VARIABLES.md](/docs/ENVIRONMENT_VARIABLES.md).

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

> **NOTE:** If you want to play around with the Nginx configuration you need to reload the Nginx Plus server with `./bin/releoad-nginx`.

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

### Making API Requests

A ready to use Postman collection can be found [here](/docs/assets/postman/Approov_Nginx_Plus.postman_collection.json). 

> **NOTE:** The collection was tailored for this Approov integration example, thus it will not work with the Approov integration in your own API backend, and requires environment variables on the [.env.example](/.env.example), that are automatically set by the Docker stack.

#### With an Approov Token Header

From a **shell in your host machine**, run:

```
curl -X GET \
  http://pdm.approov.io:8002/api/approov-token-protected \
  -H 'Accept: */*' \
  -H 'Approov-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjQ3MDg2ODMyMDUuODkxOTEyfQ.c8I4KNndbThAQ7zlgX4_QDtcxCrD9cff1elaCJe9p9U' \
  -H 'Cache-Control: no-cache'
```

We should get a response similar to this:

```json
{
  "hostname": "630ecd2b4af5",
  "status": "APPROOV_TOKEN_PROTECTED"
}
```

#### With an Approov Token Header that Includes a Tokend Binding to the Authorization Header

From a **shell in your host machine**, run:

```
curl -X GET \
  http://pdm.approov.io:8002/api/approov-token-binding-protected \
  -H 'Accept: */*' \
  -H 'Approov-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjQ3MTgwMTgyMjQuNzgwMzY4LCJwYXkiOiJWUUZGUEpaNjgyYU90eFJNanowa3RDSG15V2VFRWVTTXZYaDF1RDhKM3ZrPSJ9.N-KwuLeUt9s6TDibhX32AIkhobCYVh5-brVESqUxdBk' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Cache-Control: no-cache'
```

We should get a response similar to this:

```json
{
  "hostname": "630ecd2b4af5",
  "status": "APPROOV_TOKEN_BINDING_PROTECTED"
}
```

### Cleanup

When you are done with testing the Approov Integration with Nginx Plus or you just want to restart from a clean state, just completely remove it from your system:

```
./bin/uninstall 
``` 

Basically we will stop and remove the docker container for Centos and Backend, and also the official docker images for `centos:7` and `python:3.8-slim`, plus the custom built for `approov/backend`.

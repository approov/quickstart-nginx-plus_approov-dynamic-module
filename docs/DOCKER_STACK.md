# DOCKER STACK

A more detailed explanation about using the Docker stack to play around with Approov Integration with Nginx Plus.

We will use the official Docker container for Centos 7, and install on it Nginx Plus and all the necessary dependencies to integrate Approov.


### Centos in a Docker Container

From your host machine run the docker container with:

```
./bin/docker-centos shell
```

and now you should have a Bash shell inside the Centos container...

> **NOTE:** Unless explicit stated, all subsequent commands must be executed from the Centos container shell.


### Installing Nginx Plus:

In order to try the Approov integration with Nginx Plus we are using a throw away Centos container, and for this exercise we assume that the Nginx Plus Certificates are located at `/etc/ssl/nginx` on your host machine.

```
./bin/install-nginx-plus
```

> **NOTE:** The script follows the official [docs](https://cs.nginx.com/repo_setup) to install Nginx Plus in Centos 7.

#### Starting Nginx Plus:

```
nginx
```

Visit the url of your server at the port you have started the container with, defaults to `8002`, that in local development will be http://localhost:8002, and you will see the default Nginx `index.html` page, meaning that we are ready to proceed to add the Approov module into Nginx.


### Build the Backend

The [backend](./backend) is a simple Python server that we will run inside a docker container, but first we need to build it, and we provide a [wrapper bash script](./bin/docker-backend) to help with managing the docker commands we need to execute.

From the **shell of your host machine**, run:

```
./bin/docker-backend build
```

Let's start the Backend so that we can test its working:

```
./bin/docker-backend up
```

Now from the **Centos container shell**, where Nginx is running:

```
$ curl approov-backend:5000/api
{"hostname":"e810140a634c","status":"NOT_APPROOV_TOKEN_PROTECTED"}
```

> **NOTE:** The `approov-backend` in the curl command its the container name used for the backend.

# PITFALLS

## CLIENT SIDE ERORRS

For all errors that are observable from the client making the request.

### Page is Unavailable

An Approov protected route is not reachable, and you can't see anything in the error log,

#### Cause

Probably some error is occurring during the request, maybe with the JWT validation.

#### Solution

You need to enable `debug` level in your Nginx configuration:

```
error_log /var/log/nginx/api.error.log debug;
```

Now you can look into the logs for the error, and then try to find the solution for it in the following pitfalls, or by Google it.

### Request Redirect to Nginx Upstream Server

When the client receives a `308` permanet redirect to an url for the upstream server declared in the Nginx configuration.

##### the http status in the header of the response:

```
HTTP/1.1 308 PERMANENT REDIRECT
```

##### the response body of the message contains:
```
You should be redirected automatically to target URL: http://apibackend/api/approov-token-protected/.
```

#### Cause

The Nginx upstream server was pointing to a backend that was returning a `308` permanent redirect status:

```
INFO:werkzeug:172.29.0.3 - - [17/Jan/2020 14:59:13] "GET /api/approov-token-protected HTTP/1.0" 308 -
```

#### Solution

I opted to fix the redirection in the backend, because the redirection was caused by a line code added for debug purposes.

##### before:

```
@api.route("/api/approov-token-protected")
@api.route("/api/approov-token-protected/")
def apiApproovTokenProtected():
```

##### after:

```
@api.route("/api/approov-token-protected")
def apiApproovTokenProtected():
```

> **NOTE**: When using `curl` add option `-i` to print out the headers in the response, thus making it easier and faster to spot some issues.


## NGINX ERRORS IN LOGS

For all errors we find in the Nginx logs.

### Invalid JWT HS key

Line in logs:

```
2020/01/17 14:05:42 [info] 1293#1293: *62 invalid JWT HS key, client: 109.48.104.109, server: , request: "GET /api/approov-token-protected HTTP/1.1", host: "nginx-plus-demo.example.com:8002
```

#### Cause

The secret to verify and decode the JWT secret is not encoded in base64 safe url format.

#### Solution

The secret provided to verify the JWT signature must be base64 url safe encoded:

So if you have a normal base64 encoded one, just do:

```
echo "h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==" | base64 -d | base64url
h-CX0tOzdAAR9l15bWAqvq7w9olk66daIH-Xk-IAHhVVHszjDzeGobzNnqyRze3lw_WVyWrc2gZfh3XXfBOmww==
```

> **NOTE**: In linux the `base64url` command is available form package `basez`.

Now update the secret in the JWT key file you have defined for `auth_jwt_key_file` in your Nginx configuration.

# ENVIRONMENT VARIABLES

This is required to integrate [Approov Token](https://www.approov.io/docs/v2.1/approov-usage-documentation/#approov-tokens) check on your own Nginx Plus server, but if your are following along the Approov integration example from the [README.md](/README.md), then this isn't required, because the Docker stack its setting them by using the [.env.example](/.env.example) file.


## APPROOV SECRET

The Approov secret used in this document and in the [.env.example](/.env.example) file its not a production secret, aka, obtained via the [Approov CLI tool](https://www.approov.io/docs/v2.1/approov-cli-tool-reference/#secret-command), instead it was generated with OpenSSL.

### Generate an Approov Secret for Test Purposes

To generate an Approov base64 secret for testing from Curl, Postman or similar tools:

```
$ openssl rand -base64 64 | tr -d '\n'; echo
h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==
```

> **IMPORTANT:**
>
>For a production backend you will need to use the [Approov CLI tool](https://www.approov.io/docs/v2.1/approov-cli-tool-reference/#secret-command):
>
>```
>approov secret /path/to/approov/administration.token -get
>```

### Set the Approov Base64 Secret

```
export APPROOV_BASE64_SECRET=h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==
```

### Set the Approov Token Binding Header Name

Set the environment variable with:

```
export APPROOV_TOKEN_BINDING_HEADER_NAME=Authorization
```

### Confirming that the Variables are in the Environment

We confirm they are set with:

```
$ env | grep APPROOV -
APPROOV_BASE64_SECRET=h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==
APPROOV_TOKEN_BINDING_HEADER_NAME=Authorization
```

> **ALERT:**
>
> In a production system where Nginx is started with the `systemctl` command, all variables that we can see with command `env` aren't available, instead it can only access variables that are observable with the `systemctl show-environment` command.
>
>In order to set the Approov base64 secret as an environment variable with `systemctl` we need to do:
>
>```
>systemctl set-environment APPROOV_BASE64_SECRET=h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==
>```
>
>```
>systemctl set-environment APPROOV_TOKEN_BINDING_HEADER_NAME=Authorization
>```
>
>and now we can confirm with:
>
>```
>$ systemctl show-environment
>APPROOV_BASE64_SECRET=h+CX0tOzdAAR9l15bWAqvq7w9olk66daIH+Xk+IAHhVVHszjDzeGobzNnqyRze3lw/WVyWrc2gZfh3XXfBOmww==
>APPROOV_TOKEN_BINDING_HEADER_NAME=Authorization
>```

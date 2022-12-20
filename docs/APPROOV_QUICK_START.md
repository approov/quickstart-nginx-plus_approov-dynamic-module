# APPROOV QUICK START

This quick start is for developers familiar with NGINX Plus who are looking for a quick intro into how they can add [Approov](https://approov.io) into an existing project. Therefore this will guide you through the necessary steps for adding Approov to an existing NGINX Plus instance.

We strongly advise you to try first this quick start in a development environment, and just follow it in a production environment when you understand how Approov works within your NGINX Plus deployment.

## APPROOV CLI TOOL

If you haven't done it already, please follow [these instructions](https://approov.io/docs/latest/approov-installation/#approov-tool) from the Approov docs to download and install the [Approov CLI Tool](https://approov.io/docs/latest/approov-cli-tool-reference/).

Don't forget to enable your Approov `admin` role with:

```bash
eval `approov role admin`
````

For the Windows powershell:

```bash
set APPROOV_ROLE=admin:___YOUR_APPROOV_ACCOUNT_NAME_HERE___
```

## APPROOV API

Approov needs to know the domain name for the API its authorized to issue valid tokens.

Add it with:

```
approov api -add your.api.domain.com
```

> **NOTE:** By default a symmetric key (HS256) is used to sign the Approov token on a valid attestation of the mobile app for each API domain it's added with the Approov CLI, so that all APIs will share the same secret and the backend needs to take care to keep this secret secure.
>
> A more secure alternative is to use asymmetric keys (RS256 or others) that allows for a different keyset to be used on each API domain and for the Approov token to be verified with a public key that can only verify, but not sign, Approov tokens.
>
> To implement the asymmetric key you need to change from using the symmetric HS256 algorithm to an asymmetric algorithm, for example RS256, that requires you to first [add a new key](https://approov.io/docs/latest/approov-usage-documentation/#adding-a-new-key), and then specify it when [adding each API domain](https://approov.io/docs/latest/approov-usage-documentation/#keyset-key-api-addition). Please visit [Managing Key Sets](https://approov.io/docs/latest/approov-usage-documentation/#managing-key-sets) on the Approov documentation for more details.

Now that Approov knows the domain for your API you get [dynamic certificate pinning](https://approov.io/docs/latest/approov-usage-documentation/#dynamic-pinning) out of the box for free.


## APPROOV SECRET

We need an [Approov secret](https://approov.io/docs/latest/approov-cli-tool-reference/#secret-command) to check the signature in the JWT tokens and we need to use the same one used by the [Approov Cloud service](https://www.approov.io/approov-in-detail.html) to sign the [Approov Tokens](https://www.approov.io/docs/latest/approov-usage-documentation/#approov-tokens) issued to our mobile app.

### Retrieve the Approov Secret

```
approov secret -get base64url
```

> **NOTE:** The `approov secret` command requires an [administration role](https://approov.io/docs/latest/approov-usage-documentation/#account-access-roles) to execute successfully.

### Set the Approov Secret Unique Key Identifier(KID)


The `kid` identifier must be presented in the JWT header of any Approov Token we want to verify, otherwise Nginx will not know what secret to use to verify it, and the validation will fail.

So set it in the Approov cloud service with this command:

```
approov secret -setKeyID 0001
```

> **NOTE:** The `approov secret` command requires an [administration role](https://approov.io/docs/latest/approov-usage-documentation/#account-access-roles) to execute successfully.

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


## NGINX CONFIGURATION

### Add the Approov Secret to the Nginx key File 

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

### Add the Check for the Approov Token

Checking for a valid Approov Token couldn't be easier to do, just add two lines to the `server` block configuration for the endpoint you want to protect.

```nginx
# All API endpoints for `/api/v2/*` are protected with an Approov Token check.
location /api/v2 {

    # ADD THIS TWO LINES:
    auth_jwt   "APPROOV" token=$http_Approov_Token;
    auth_jwt_key_file approov-secret.jwk;
    
    # rest of your nginx configuration...
}
```

This configuration will enforce that any request for `api/v2/*` *MUST* provide a valid Approov Token in the header `Approov-Token`, otherwise the request will be denied.


## TESTING THE APPROOV TOKEN CHECK IN NGINX PLUS

### Requests with an Approov Token 

#### Valid Approov Token Header 

This request example is for a valid Approov Token.

##### request:

```
curl -i -X GET \
  https://your.api.domain.com/api/v2 \
  -H "Approov-Token: $(approov token -genExample your.api.domain.com | head -1)"
```

##### response:

```
HTTP/1.1 200 OK
Server: nginx/1.17.6
...
```

#### Invalid Approov Token Header 

This request example is for an invalid Approov Token.

##### request:

```
curl -i -X GET \
  https://your.api.domain.com/api/v2 \
  -H "Approov-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJleHAiOjQ3MDg2ODM0NTcuNDg1Mzk1LCJwYXkiOiI1NjZ2UVdhV0dCZ3MrS0U4eXNqVFRQUXRncHVlK1hMTXF4OGVZb2JDckkwPSJ9.5tsHeglDEv_89lPVKjCmMWrfPW3phvcgDEGlNn7ZACU"
```

##### response:

```
HTTP/1.1 401 Unauthorized
Server: nginx/1.17.6
...
```

# Pick axe Oauth provider.

## Tenant API.
Tenant API has operations to create a new tenant.

### Register a new tenant
Tenenacy is more like realm, it defines the context of a particular customer.
To register a tenant use,

```
curl --location --request POST 'http://localhost:5000/api/tenant' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "nilk",
    "description": "lorem ipsum dolor set amet.",
    "tenant_logo_url": "https://s3::00000000000001:local.png"
}'
```


### Get the public key info from issuer endpoint.
All the tokens are generated via a private key that is stored in AWS secrets manager, the token
decoding would require a issuer URL to publically host a public KEY.
This is the issuer URL.

```
curl --location --request GET 'http://localhost:5000/api/tenant/nilk/auth' \
--data-raw ''
```

## OAuth client API.
APi endpoints to register oauth endpoints.

TODO...


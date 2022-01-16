# Pickaxe Oauth provider.

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
Api endpoints to register oauth endpoints.
<i>Supported grant types are client credentials, password, auth code grant.</i>

```
curl --location --request POST 'http://localhost:5000/api/oauth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "lorem",
  "grant_type": "client_credentials",
  "tenant": "nilk",
  "allowed_scopes": "[]"
}'
```

## Token API.
Api endpoints to get the token for a particular oauth grant type.
<i>Supported grant types are client credentials, password, auth code grant.</i>

Refer to grant schemas in the doc

```
curl --location --request POST 'http://localhost:5000/api/tenant/nilk/token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "client_id": "2f9ae025-7a59-4cd0-8405-6d0c846b7bf5",
    "client_secret": "62f03c60771911ec8a320242ac110002",
    "grant_type": "client_credentials",
    "audience": []
}'
```

<b>How to verify if the token is valid ?</b>

#### Usage of the token introspection endpoint
Use the token introspection endpoint to verify the vaidity if the token.
```
curl --location --request GET 'http://localhost:5000/api/tenant/nilk/introspect' \
--header 'Content-Type: application/json' \
--data-raw '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwOi8vaHViLmRvY2tlci5pbnRlcm5hbDo1MDAwL2FwaS90ZW5hbnQvbmlsay9hdXRoIiwiZXhwIjoxNjQyMzc2MDk5LjY0NTM0NywibmJmIjoxNjQyMzcyNTA5LjY0NTM1NywiaWF0IjoxNjQyMzcyNTA5LjY0NTM2MzgsImp0aSI6MTY0MjM3MjQ5OS42NDUzNjk1LCJhdWQiOltdfQ.Qv9fIQdTeoP0x5OqHs8RqC-blligYQxVDntTwHoQr8O4czHM25tJMw9xOpji2s6oy9FrXm-7q-kAWwbsCKTxDLwMUpygRCzk-nAZf6ghh9cM2tBwlDIBuoCAT4HsE1r_Znw8wn3YkSkfh7qztgWClIMU2m98vtSA8hvSrUYggtPxSyXIYzJ1a2Jo3GHFbIwHSooY0HCTfaRRLLSPoFfO_z2wGteBrezk56q1ub2sdU4LqTwBR9pmgLttfT8tMsuXA5JXk2SbnZ76zenSU9UxJ-ZDAAaLWnjU48R_lxzpoPWCsRKDcq5KwDNfAEDG61tcSiNKomaBxQO8QrPHOmM3A"
}'
```

### Setup on postman?
Find the postmark collection, go to folder `./postman` and import the postman collection in Postman.
Enjoy testing in QA.


### API Documentation
The application API doc is auto generated and can be accessed @ 
`HOST:PORT/api/doc`
```
HOST: server host
PORT: 5000
```
![image](https://user-images.githubusercontent.com/68027670/149682249-84e14710-f637-4100-b65b-eabf71454da0.png)


### Supported grant types

- <b>Authcode grant</b>: 
This is the flow that regular web apps use to access an API. Use this endpoint to exchange an Authorization Code for a Token.
```
'auth_code': {
        'client_id': string,
        'client_secret': string,
        'audience': array,
        'username': string,
        'password': string,
        'scopes': array,
        'code': string
        'redirect_urls': array
    }
```

- <b>Client Credentials grant </b>:
This is the OAuth 2.0 grant that server processes use to access an API. Use this endpoint to directly request an Access Token by using the Client's credentials (a Client ID and a Client Secret). Very suited for Machine to Machine Auth.
```
'auth_code': {
    'client_id': string,
    'client_secret': string,
    'audience': array
}
```

- <b>Resource owner password grant </b>:
This is the OAuth 2.0 grant that highly-trusted apps use to access an API. In this flow, the end-user is asked to fill in credentials (username/password), typically using an interactive form in the user-agent (browser). This information is sent to the backend and from there to Auth0. It is therefore imperative that the application is absolutely trusted with this information.
```
'auth_code': {
    'client_id': string,
    'client_secret': string,
    'audience': array,
    'username': string,
    'password': string,
    'scopes': array
}
```


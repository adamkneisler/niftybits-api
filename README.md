# Getting your dev env running

## Build and run docker image

```
docker build -t nifty-api .

docker run -v ~/niftybits-api:/usr/src/app -p 8000:8000 -t nifty-api
```

Where `~/niftybits-api` is the absolute path to your code directory


# API Docs

## Authentication

### **GET** - /auth/twitter/token/

#### This will return an oauth token to be used to authorize Twitter to get the oauth verifier back

### Successful Response

```
{
  "oauth_token": "A4Ue-QAAAAABVR9gAAABfRv2f5A"
}
```

### **POST** - /auth/twitter/

#### This endpoint takes the oauth_token and oauth_verifier as the JSON body to return the user oauth_token and twitter user_id

### Request Body

```
{
  "outh_token": "2lkljdlksdf882934jsdf",
  "oauth_verifier": "23lkj4lkjls008sdksf",
}
```


### Successful Response

```
{
  "user_id": "1111111",
  "token": "2lkljdlksdf882934jsdf",
}
```


## Sample endpoint

### **GET** - /hello/

#### Use the token returned from the Twitter auth call to create an Authorization header for all requests

### Example Headers

```
{
    "Authorization": "Token: 2lkljdlksdf882934jsdf"
}
```

### Successful Response

```
{
  "message": "Hello, World!"
}
```

### Error Response

```
{
  "detail": "Invalid token."
}
```
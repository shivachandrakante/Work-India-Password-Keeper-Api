# PASSWORD_KEEPER

## Use of this API

*__An awesome package which helps us in saving the websites username and passwords in encoded format. 
We can retrieve the passwords by logging in.__*

---

## Installation
``` bash
pip install password_keeper
``` 

## How to use it?

## Endpoints

1. User account registration:

```
[POST] /app/user

Request Data: {
    'username': str,
    'password': str
}

Response Data: {
    'status': 'account created'
}

```

## Test


2. User account login

```
[POST] /app/user/auth

Request Data: {
    'username': str,
    'password': str
}

Response Data: {
    'status': 'success',
    'userId': int
}

```

3. List Saved Passwords

```
[GET] /app/sites/list/?user={userId}

Request Data: None
Response Data: [List of stored website username & passwords]

```

4. Save a new Passwod:

```
[POST] /app/sites?user={userId}

Request Data: {
    'website': str,
    'username': str,
    'password': str
}

Response Data: {
    'status': 'success'
}


```
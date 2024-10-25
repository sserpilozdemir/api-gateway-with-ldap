# API Gateway 

> Python 3.11
> Flask 
> Docker - Bitnami(LDAP)

# Features

> Auth with ldap
> caching with redis lib
> limiter (throttle handler) 

## Run

```console
$ python app.py
```

## Useful Information

[Quick Start flask_ldap3_login](https://flask-ldap3-login.readthedocs.io/en/latest/quick_start.html)

[Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)

## Postman Collection

## Long Term Goals
> Running in one container all services like redis, openldap, flask app (and same network)
> focusing async programming (in same container flask app has to wait other services running)
> creating robust unit testing 
> creating strong folder structure and following python design patterns

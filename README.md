# Matching Melodies 

Matching Melodies is online service that allows musicians to find opportunities: discover events to perform at or search for like-minded musicians.


## Installation

1. create repository locally
    ```
    git clone https://github.com/mamula2023/matching_melodies.git
    cd matching_melodies
    ```
3. activate virtual environment
4. install requirements
    ``` 
    pip install -r requirements.txt 
    ```
5. make migrations
    ```
    python manage.py migrate
    ```
6. Run server 
    ``` 
    python manage.py runserver PORT
    ```
     By default, django server runs on port 8000


## Endpoints    

POST /api/users/
```json
{
    "email": "example@example.com", 
    "username": "username",
    "password": "password",
    "bio": "bio",
    "website": "example.com",
    "role": "organizer"
}
```
* email: valid email strcuture
* website: empty or valid website structure
* valid roles: ```organizer```, ```musician```

POST /user/token/
* request:
```json
{
    "email": "example@example.com",
    "password": "password"
}
```
* response:
```json
{
    "access": "access_token",
    "refresh": "refresh_token"
}
```
GET /api/user/{:id}/
    -H "Authorizaion: Bearer <ACCESS_TOKEN>"

* Make sure to provide with valid access_token returned in /user/token/

returned user structure:
```json
{
    "id":           1,
    "email":        "example@example.com",
    "username":     "username",
    "bio":          "bio",
    "website":      "example.com",
    "profile_pic": "url_to_image.com",
    "role":         "organizer",
    "coins":        100
}

* Note, `email` and `coins` are returned only if client is asking information about itself 















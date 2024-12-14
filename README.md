
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














=======
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
1. Create new user 
	```
	POST /api/users/ \
	-H "Content-Type: multipart/form-data" \
	-F "email=example@example.com" \
	-F "username=username" \
	-F "password=password" \
	-F "bio=bio" \
	-F "website=www.example.com" \
	-F "role=organizer" \
	-F "profile_pic=@/path/to/image.jpg"
	```
	
	* email: valid email format
	* website: empty or valild website format
	* valid roles: ```organizer```, ```musician```

2. Acquire access and refresh tokens for JWT authentication
	`POST /user/token/`
	* request body:
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
3. List all users, or retrieve individual user by id
	```
	GET /api/user/{:id}/ \
	-H "Authorizaion: Bearer <ACCESS_TOKEN>"
	```
	* Make sure to provide with valid access_token acquired in `/user/token/`
	
	* response body of a single user:
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
	```
	* Note, `email` and `coins` fields are returned only if client is asking information about itself 

4. Create new event 
	```
	POST /api/event/
	-H "Authorization: Bearer <ACCESS_TOKEN>" \
	-H "Content-Type: multipart/form-data" \
	-F "title=title of event" \
	-F "description=$description of the event" \
	-F "city=Tbilisi" \
	-F "location=exact address of event" \
	-F "payment=100" \
	-F "additional_info=any additional inforamtion" \
	-F "img=@/path/to/image.jpg" \
 	-F "categories=1" \
 	-F "categories=3" \
 	-F "genres=2" \
	```

5. Get all events or retrieve one by id
	```
	GET /api/event/{:id}/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>"
	```
	* response body of a single event
	```json
	{
	  "id": 1,
	  "title": "title",
	  "description": "description of event",
	  "city": "city",
	  "location": "exact location of the event",
	  "img": "url_to_image.gom",
	  "payment": 100,
	  "additional_info": "additional_info",
	  "categories": [
		{
		  "id": 3,
		  "title": "Bar"
		},
		{
		  "id": 4,
		  "title": "Cafe"
		}
	  ]
	  "genres": [
		{
		  "id": 1,
		  "title": "Hip-Hop"
		},
		{
		  "id": 2,
		  "title": "Pop"
		}
	  ]  
	}
	```





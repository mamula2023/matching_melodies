***
The backend of the project is nearly complete and functions as intended. However, the frontend is quite basic and mainly displays information, with limited interactivity and not all backend functionality integrated yet. Any contributions, especially in the form of pull requests for the backend and frontend, are welcome.
***

# Matching Melodies 

Matching Melodies is online service that allows musicians to find opportunities: discover events to perform at or search for like-minded musicians.

## Installation

1. create repository locally
  ```
  git clone https://github.com/mamula2023/matching_melodies.git
  cd matching_melodies
  ```

3. activate virtual environment

  * using venv
    ```
    python -m venv venv
    source venv/bin/activate
    ```
  * using anaconda

    * create environment
    ```
    conda create -n [your env name] python=3.11
    ```
    * activate
    ```
    conda activate [your env name]
    ```
4. install requirements
  ``` 
  pip install -r requirements.txt 
  ```

5. install redis server for celery
  * using apt on linux
  ```
  apt update
  apt install redis
  ```
  * and start server by
  ```
  redis-server
  ```

7. make migrations
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
8. populate .env
    
  To send informational emails to applicants when their status changes (accepted or rejected),
  the system currently uses my personal email credentials.
  If you want to test the project, you'll need to populate the missing fields in the .env file as follows:
  ```
  EMAIL_HOST_USER=
  DEFAULT_FROM_EMAIL=
  ```
   Generate an app password in your Google account settings:
  
   Go to Google Account Settings.
   Under "Security," find "App passwords."
   Create a new app password for your application and copy the 16-character password provided.
   ```
   EMAIL_HOST_PASSWORD=
   ```

9. set up celery tasks
  * in separate terminals run:
  ```
  celery -A matching_melodies worker
  celery -A matching_melodies beat
  ```

10. Run server 
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
    GET /api/user/{:id/} \
    -H "Authorizaion: Bearer <ACCESS_TOKEN>"
    ```
    * Make sure to provide with valid access_token acquired in `/user/token/`
    * listing all users without particular id returns paginated result
    ```json{
      "count": 10, 
      "next": "url_to_next_pagination",
      "previout": "url_to_prev_pagination",
      "results": [
        {
          ...
        },
        {
          ...
        },
        ...
      ]
    ```
    * can be filtered by: `role`
    * can be ordered by: `created_at`, `username`. By default: `created_at`
    
    * response body of a single user:
    ```json
    {
      "id":           1,
      "email":        "example@example.com",
      "username":     "username",
      "bio":          "bio",
      "website":      "example.com",
      "profile_pic":  "url_to_image.com",
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
    -F "date=2024-01-01" \
    -F "payment=100" \
    -F "event_type=gig" \
    -F "additional_info=any additional inforamtion" \
    -F "img=@/path/to/image.jpg" \
    -F "categories=1" \
    -F "categories=3" \
    -F "genres=2" \
    ```
    * possible event types: `gig` and `collaboration`
    * `gig` can only be created by organizers
    * `collaboration` can only be created by musicians
    * field `date` is only for gigs. collaborations are meant to be long-term continuous process
    * after date of `date` has passed, all applications on event will have status changed to `performed`

5. Get all events or retrieve one by id
    ```
    GET /api/event/{:id}/?author=1&city=Tbilisi \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
    ```
    * listing all events implement pagination (refer to listing users)
    * available fiters: `genres`, `categories`, `author`, `city`, `event_type`
    * can be ordered by `created_at`, `payment`, `title`, `date`. By default: `created_at`

    * response body of a single event
    ```json
    {
      "id": 1,
      "title": "title",
      "description": "description of event",
      "city": "city",
      "location": "exact location of the event",
      "date": "2025-01-01T00:00:00Z",
      "img": "url_to_image.gom",
      "payment": 100,
      "additional_info": "additional_info",
      "event_type": "gig", 
      "created_at": "2024-12-20T20:12:15.805916Z",
      "updated_at": "2024-12-21T12:00:45.000000Z",
      "author": 1,
      "categories": [
          {
            "id": 3,
            "title": "Bar"
          },
          {
            "id": 4,
            "title": "Cafe"
          }
        ],
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
6. Apply for event as musician
   ```
   POST /api/event/:id/apply/ \
   -H "Authorization: Beear <ACCESS_TOKEN>"
   ```
   User that is applying must be registered as musician.
   Response with appropriate message is returned

7. List applications on event
   ```
   GET /api/event/:id/application/ \
   -H "Authorization: Bearer <ACCESS_TOKEN>"
   ```
   Only author of event is able to see applications on the event
   * implements pagination (refer to events and applications endpoints)
   * can be filtered by `user`, `event`

8. See application of particular ID
   ```
   GET /api/application/:id/ \
   -H "Authorization: Bearer <ACCESS_TOKEN>"
   ```
   This endpoint is only available if user who applied is accessing, or author of event on which application is made

9. Accept or reject application
    ```
    POST /api/event/application/:id/{action}/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
    ```
    * {action} is either accept or reject
    * Accepting or rejecting can only be done once.
    * hitting endpoint triggers celery task that notifies applicant about status change

10. Get available genres and categories
    ```
    GET /api/event/genre/
    GET /api/event/category/
    ```
    These endpoints do not need authorization. Genre and Category objects are added only by admin in admin panel.
    These endpoints return arrays of corresponding objects
    Single object in response:
    ```json
    {
      "id": 1,
      "title": "Hip-Hop"
    }
    ```

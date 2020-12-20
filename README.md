# FSND_Capstone
## Final Project for Udacity's Full-Stack Nanodegree Program

### The Premise

This project is focused on building out the back-end programming needed for a functional website.  In this casting company example, actors and movies are added, modified, and removed from the database by different users with different permissions.

### The Project

The app does the following:

1) Display actors and movies. 
2) Delete actors and movies.
3) Add actors and movies.
4) Modify existing actors and movies.

# Getting Started

```bash
# First, Python 3 must be installed
# Second, install requirements
pip install -r requirements.txt
# Create the postgres database
psql -U <username> postgres < postgres.psql
```
To run unit tests to ensure expected functionality:
```bash
dropdb postgres (for Windows: drop database postgres)
createdb postgres (for Windows: create database postgres)
psql postgres < postgres.psql
python unit_test.py
```

# API Reference
## Notes
1. This app can be run locally as well as on Heroku.  The Heroku version is running at https://fsnd-capstone-2.herokuapp.com/.
2. The app requires authentication tokens, which are located in the .env and setup.sh files per role.
3. CORS is enabled.

## Error Handling
Errors are returned as JSON objects in the following format:
```bash
{
  "success": False,
  "error": 400,
  "message": "Bad Request"
}
```
The API will return four error types when requests fail:
1.  400: Bad Request
2.  404: Not Found
3.  422: Unprocessable Entity
4.  500: Internal Server Error

# Roles and Permissions
## Casting Assistant - Can view actors and movies
### Permissions
* Get:actors
* Get:movies

## Casting Director - All permissions a casting assistant has, add or delete an actor from the database, and modify actors or movies
### Permissions
* Get:actors
* Get:movies
* Post:actors
* Delete:actors
* Patch:actors
* Patch:movies

## Executive Producer - All permissions a casting director has and add or delete a movie from the database
### Permissions
* Get:actors
* Get:movies
* Post:actors
* Delete:actors
* Patch:actors
* Patch:movies
* Post:movies
* Delete:movies


# Endpoints
### GET /actors
* General
  * Request Parameters: None
  * Returns a dictionary of actors where each has an ID and descriptive text.
  * Returns success status.
  * Requires permission "get:actors"
*
```bash
reponse = {
success: True,
actors: [
          {
            name: "Imaf Atcow",
            age: 60,
            gender: "male"
          }
        ]
  }
```

### GET /movies
* General
  * Request Parameters: None
  * Returns a dictionary of movies where each has an ID and descriptive text.
  * Returns success status.
  * Requires permission "get:movies"
* Sample: `curl http://localhost:5000/api/questions`
```bash
response = {
success: True,
movies: [
          {
            title: "Elf",
            year: 2003,
            month: 10,
            day: 9,
            genre: "comedy"
          }
        ]
  }
```

### POST /actors
* General
  #### Create Actor ####
  * Creates a new actor from user input.
  * Request Parameters: Actor form data in application/json type
  * Returns success status, and actor data.
  * Requires permission "post:actors"
*
```bash
payload = {
            name: "Imaf Atcow",
            age: 60,
            gender: "male"
          },
response = {
  success: True,
  actor:{
    name: "Imaf Atcow",
    age: 60,
    gender: "male"
   }
}
```

### POST /movies
* General
  #### Create Movie ####
  * Creates a new movie from user input.
  * Request Parameters: Movie form data in application/json type
  * Returns success status, and movie data.
  * Requires permission "post:movies"
*
```bash
payload = {
            title: "Elf",
            year: 2003,
            month: 10,
            day: 9,
            genre: "comedy"
          },
response = {
  success: True,
  movie:{
            title: "Elf",
            year: 2003,
            month: 10,
            day: 9,
            genre: "comedy"
          }
}
```

### DELETE /actors/<int:actor_id>
* General
  * Request Parameters: actor_id
  * Returns actor_id of deleted question and success status.
  * Requires permission "delete:actor"
```bash
parameters = <int:actor_id>

response = {
  success: True,
  delete: actor_id
}
```

### DELETE /movies/<int:movie_id>
* General
  * Request Parameters: movie_id
  * Returns movie_id of deleted question and success status.
  * Requires permission "delete:movie"
```bash
parameters = <int:movie_id>

response = {
  success: True,
  delete: movie_id
}
```

### PATCH /actors/<int:actor_id>
* General
  #### Patch Actor ####
  * Modifies an existing actor from user input.
  * Request Parameters: Actor form data in application/json type
  * Returns success status, and actor data.
  * Requires permission "patch:actors"
*
```bash
payload = {
            name: "Bob Dole",
            age: 80,
            gender: "male"
          },
response = {
  success: True,
  actor:{
    name: "Bob Dole",
    age: 80,
    gender: "male"
   }
}
```

### PATCH /movies/<int:movie_id>
* General
  #### Patch Movie ####
  * Modifies an existing movie from user input.
  * Request Parameters: Movie form data in application/json type
  * Returns success status, and movie data.
  * Requires permission "patch:movies"
*
```bash
payload = {
            title: "Elf",
            year: 2003,
            month: 10,
            day: 9,
            genre: "comedy"
          },
response = {
  success: True,
  movie:{
            title: "Elf",
            year: 2003,
            month: 10,
            day: 9,
            genre: "comedy"
          }
}
```

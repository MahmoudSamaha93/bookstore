# Dockerization of Bookstore Web API (Python Flask) with MySQL

## Description

Bookstore Web API Application aims to create a bookstore web service using Docker to give students the understanding to dockerization of an application. The application code is to be deployed as a RESTful web service with Flask using Dockerfile and Docker Compose on GitHub using Terraform.

| HTTP Method  | Action                                                                    | Example                            |
| --- |---------------------------------------------------------------------------|------------------------------------|
| `GET`     | Retrieves list of all books                                               | http://localhost:8000/books        |
| `GET`     | retrieves book with specific ISBN                                         | http://localhost:8000/books/1234-5 |
| `POST`    | Insert a new book, from data provided with the request                    | http://localhost:8000/books        |
| `PUT`     | Updates the book with a specified id, from data provided with the request | http://localhost:8000/books/123    |
| `DELETE`  | Delete the book with a specified id                                       | http://localhost:8000/books/123    |


## Project Skeleton

```text
bookstore (folder)
|
|----word_occurrences (folder)
|    |
|    |----book.txt
|    |----Dockerfile
|    |----main.py
|----bookstore.tf            
|----bookstore-api.py   
|----docker-compose.yml 
|----Dockerfile
|----MOCK_DATA.csv 
|----readme.md          
|----requirements.txt   
```

### HOW TO RUN?

##### Run the command `docker-compose up` to start containers.

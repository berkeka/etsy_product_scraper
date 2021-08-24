# Etsy product scraper

This project allows users to input a etsy product url then saves te product info to a database. Project uses Flask for the backend, bootstrap for frontend and Postgresql as the database.

## Installation

First you need to create a file named .env in the root directory of the project. This file should include your secret key.

Example:
```
SECRET_KEY=YOUR_SECRET_KEY
```

Now you can build and run the project using docker-compose.

```bash
docker-compose build
docker-compose up 
```

Project can be accessed from `localhost:5000/`

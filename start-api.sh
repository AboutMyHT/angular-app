#!/bin/bash

# Check if the container "my-local-mysql" exists
if docker ps -a -q --filter "name=my-local-mysql" > /dev/null 2>&1; then
  # Stop and remove the container if it exists
  docker stop my-local-mysql > /dev/null 2>&1
  docker rm my-local-mysql > /dev/null 2>&1
fi

# Run the MySQL container
docker run --name my-local-mysql -e MYSQL_ROOT_PASSWORD=localpass -e MYSQL_DATABASE=mydb -p 3306:3306 -d mysql:latest --default-authentication-plugin=mysql_native_password

# Change directory and start the SAM local API
cd aboutmyhometown-lambda-stack && (
    sam local start-api -p 4201
)

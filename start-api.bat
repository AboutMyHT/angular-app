@echo off
docker ps -a -q --filter "name=my-local-mysql" >nul 2>&1
if %errorlevel% == 0 (
  docker stop my-local-mysql >nul 2>&1
  docker rm my-local-mysql >nul 2>&1
)


docker run --name my-local-mysql -e MYSQL_ROOT_PASSWORD=localpass -e MYSQL_DATABASE=mydb -p 3306:3306 -d mysql:latest --default-authentication-plugin=mysql_native_password

cd aboutmyhometown-lambda-stack && (
    sam local start-api -p 4201
)

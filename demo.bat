:: Open api documentation page
start api_documentation.html

:: Build docker image and start application inside a docker container
start docker-compose up

:: Make curl request to the api of the application; continue when application is running
:repeat
    (curl localhost:8000/clear_blacklist | find "true") || goto :repeat

:: Run all tests
python -m unittest tests.py
pause

:: Close application
docker-compose down
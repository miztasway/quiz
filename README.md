# Quiz
This is a quiz app built with django and vuejs. It is a group assignment

## Features
    1. Every authenticated user can create a quiz
    2. Every authenticated can answer a quiz only once
    3. Scores gotten for a right answer is subject to the time it took to answer the question
    4. Quizzes are conducted by the frontend. The backend only stores the data involved



## Steps to test
1. Clone this repository `https://github.com/Joetib/quiz.git`. There are two branches here. `master` and   `dev`.
To contribute, make sure you clone the dev branch.
2. Create a python virtual environmen
    ```cmd
    c:>.../quiz/> python -m venv venv
    c:>.../quiz/> call venv/scripts/activate
    c:>.../quiz/> pip install -r requirements.txt
    ```
3. change directory into the server folder and run the test server using

    ```
    C:>/quiz> cd server
    C:>.../quiz/server> python manage.py makemigrations && python manage.py migrate
    C:>.../quiz/server> python manage.py runserver
    ```
4. Wait for the server to start and open your browser to `127.0.0.1:8000` or `localhost:8000` 
5. Test the stuff out mate...
6. Note that all contributions should be pushed to the `dev` branch.
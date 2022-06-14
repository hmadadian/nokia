# Introduction
Based on the task that Mr. Bence Haller from Nokia in Hungary sent me, I should develop a rest API service running in Kubernetes for CRUD operations executed on the meals table. Meals contain name, price, ingredients, spicy, vegan, gluten free, description and kcal. 

So I developed an application that is a bit more dynamic, which can send a request throw a standard POST request query or in JSON format within the request body. Also, it can filter the result/update/delete with single or multiple conditions. My solution also includes authentication and an HA solution.

# How it Works
The application contains 3 parts which will be described in different sections below!

### 1. http RestAPI:
which is handling by **fastapi** and **uvicorn** library

### 2. Token Authentication:
which is handling by **JWT** library

### 3. Database Intracation:
which is handling by **sqlalchemy** library.

# Files and Classes
There are 7 files as described below:

 1. `authentication.py`: Contain `JWTBearer`, `JWTInit` and `UserManager` classes for authenticating users and requests.
 2. `db_structure.py`: Contain `DbStructure` class for creating table and validate datas based on this class.
 3. `http_2_json.py`: Contain `Http2Json` class for converting square brackets in standard post queries to dictionary objects.
 4. `validator.py`: Contain `UserSchema`, `ParamsRequired`, `JsonBody` and `Params` class for validating http requests and data within.
 5. `pgsql.py`: Contain `SqlInteraction` class for interacting with postgresql.
 6. `main.py`: Handle `uvicorn` app and execute the application based on other objects and classes.
 7. `env.py`: Contain necessary information retrieved from os environment variable or env.txt.

# How to Run
## Run on Local Machine
### 1. Create a virtual environment

A. Create a directory (Folder)

B. Download the source codes and move to the newly created directory in step A (can clone by git)

C. Open a Terminal / Command Prompt / Powershell (based on your OS)

D. Change the directory to the newly created directory in step A

E. Create a venv environment with the below command
```
python -m venv .
```
F. Activate venv with the below command (based on your OS)
```bash
### For Command Prompt
.\Scripts\activate.bat

### For Powershell
.\Scripts\Activate.ps1

### For Linux Terminal
./Scripts/activate
```

### 2. Install dependencies and required libraries

Run the following command to install dependencies and required libraries automatically (based on your OS).
```bash
### For Windows
pip install -r .\requirements.txt

### For Linux
pip install -r ./requirements.txt
```

### 3. Modify env.txt
Modify `env.txt` to load nessary data from it to connect with postgresql.

### 4. Test
```python
> python -m pytest tests/
```

### 5. Run the application

Now it is time to run the application 

**Usage:**
```bash
> python main.py
```
## Run on Local Machine (with Docker)
### 1. Download Dockerfile
Download the DockerFile from this repo

### 2. Edit Environment Variable
Modify Environment Variable inside Dockerfile to connect with postgresql.

### 3. Build image and run.
```bash
> docker build -t restapi .
> docker run -p <exposeport>:<containerport> -d restapi 
```
## Run on cloud or cluster (with Helm)
Download the Helm files from the following git repos  
A. https://github.com/hmadadian/nokia-helm-v1  
B. https://github.com/hmadadian/nokia-helm-v2  
The difference between them is the image. The v1 uses a python image, downloads dependencies, and clones the source from GitHub. In v2, it just used the image in the docker hub that we already made in the previous section.
Also please modify values.yml with required values
```bash
> git clone https://github.com/hmadadian/nokia-helm-v1.git
> helm install nokia-test-1 ./nokia-helm-v1  
```
OR
```bash
> git clone https://github.com/hmadadian/nokia-helm-v2.git
> helm install nokia-test-2 ./nokia-helm-v2  
```

# OpenAPI Test Interface
After successfully launching the application, you can access openapi for easy testings. You can access the interface with URL and port defined in environment variables. default https://127.0.0.1:8000/docs

# How to pass data
## 1. with standard post queries
A. We should first authenticate
Default usename: **nokia**
Default password: **nokiaisbest**

```bash
> curl -X 'POST' \
  'http://127.0.0.1:8000/user/login?username=nokia&password=nokiaisbest' \
  -H 'accept: application/json' \
  -d ''
```
In the responce we should get token value and use it in header as `Authorization: Bearer `
**Important: Each token is valid for 10 minutes**

B. We can also create a new user and token
```bash
> curl -X 'POST' \
  'http://127.0.0.1:8000/user/signup?username=hamed&password=hamed' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTcyOTk3Ljk3OTQ0NzR9.ZjFbuKmuLXQxFcfiAwLk9aaQVrGzxty-glt4g2zzc0A' \
  -d ''
```
**Important: Can NOT create a username multiple times**

C. Insert Data
```bash
> curl -X 'POST' \
  'http://127.0.0.1:8000/create?name=P%C3%81COLT%20NYERS%20H%C3%9AS&price=1850&ingredients=chicken%2C%20herbs&spicy=true&vegan=false&gluten_free=false&description=Marinated%20chicken%20breast%20slices%20with%20herbs&kcal=530' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTczNDIxLjIyNTQ4ODd9.8X3w37tuna1GYbBFR8ouKqsp94PadstQrwa2LloTOWU' \
  -d ''
```
**Important: Can NOT insert same data multiple times**

D. Get Data: can be used with multiple conditions

```bash
> curl -X 'POST' \
  'http://127.0.0.1:8000/read?price=1850&kcal=530' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTczNDIxLjIyNTQ4ODd9.8X3w37tuna1GYbBFR8ouKqsp94PadstQrwa2LloTOWU' \
  -d ''
```
**Important: Without parameter it returns all data**

E. Update data in form of filter[< name of the column >]=value& update_params[< name of the column >]=new_value. This also can be used with multiple filter and update multiple values.
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/update/filter%5Bgluten_free%5D%3Dfalse%26filter%5Bname%5D%3DP%C3%81COLT%20NYERS%20H%C3%9AS%26update_params%5Bdescription%5D%3Dnew%20description%26update_params%5Bingredients%5D%3Dnew%20ngredients' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc0MjI5LjM0OTkwM30.f9BvfwNxtb7npNr0L2z9jE7yJZPjkjLzon6BFWuIRyY' \
  -d ''
```
F. Delete Data: can be used with multiple conditions
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/delete?spicy=true&vegan=false' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc0MjI5LjM0OTkwM30.f9BvfwNxtb7npNr0L2z9jE7yJZPjkjLzon6BFWuIRyY' \
  -d ''
```
**Important: if the condition did not match, no data will delete**

## 2. with json
A. We should first authenticate
Default usename: **nokia**
Default password: **nokiaisbest**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/user/login/json/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "nokia",
  "password": "nokiaisbest"
}'
```
In the responce we should get token value and use it in header as `Authorization: Bearer `
**Important: Each token is valid for 10 minutes**

B. We can also create a new user and token

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/user/signup/json/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc0NzM0LjU3NTkwNTh9.b-mkn1_cs7PyDYpCj1hx7GP6itdMwqtxL9BwXFBY6Bg' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "hamed",
  "password": "hamed"
}'
```
**Important: Can NOT create a username multiple times**

C. Insert Data
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/create/json/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc1MzY2Ljk0MzM2ODR9.WSPpN-q1qCNbEaEDEc4R39HkeJ3Jj0QFHT0_W3DFeEE' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "PÉKÁRU",
  "price": 150,
  "ingredients": "Cheese",
  "spicy": false,
  "vegan": true,
  "gluten_free": false,
  "description": "Cheese bar",
  "kcal": 300
}'
```
**Important: Can NOT insert same data multiple times**

D. Get Data: can be used with multiple conditions

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/read/json/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc1MzY2Ljk0MzM2ODR9.WSPpN-q1qCNbEaEDEc4R39HkeJ3Jj0QFHT0_W3DFeEE' \
  -H 'Content-Type: application/json' \
  -d '{
  "ingredients": "Cheese",
  "kcal": 300
}'
```
E. Update data in form of filter and update_params. This also can be used with multiple filter and update multiple values.
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/update/json/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc1MzY2Ljk0MzM2ODR9.WSPpN-q1qCNbEaEDEc4R39HkeJ3Jj0QFHT0_W3DFeEE' \
  -H 'Content-Type: application/json' \
  -d '{
  "filter": {
    "name": "PÉKÁRU",
    "gluten_free": false
  },
  "update_params": {
    "price": 200,
    "description": "test"
  }
}`
```

**Important: JSON without data will returns all data**

F. Delete Data: can be used with multiple conditions
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/delete/json/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoibm9raWEiLCJleHBpcmVzIjoxNjU1MTc1MzY2Ljk0MzM2ODR9.WSPpN-q1qCNbEaEDEc4R39HkeJ3Jj0QFHT0_W3DFeEE' \
  -H 'Content-Type: application/json' \
  -d '{
  "ingredients": "Cheese",
  "description": "test"
}'
```
**Important: if the condition did not match, no data will delete**

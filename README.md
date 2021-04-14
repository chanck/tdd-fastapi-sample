# Test Driven Development Template for Python RESTAPI server with FASTAPI framework
**By: Chung Kit Chan (email: chanck@sg.ibm.com)**
This is a template for developing RESTAPI using Python FastAPI framework. More details about FastAPI framework can be found in [FastAPI Framework](https://fastapi.tiangolo.com). 

# 1. Clone the repo & setup conda virtual environment
* The repo can be clone using <code>git clone https://github.com/chanck/tdd-fastapi-sample.git</code>
* Change directory to the clone repo with <code>cd tdd-fastapi-sample</code>
* Create local python conda virtual environment with <code>conda create -n fastapi-deploy python=3.7</code>
* Activate the newly created conda environment with <code>conda activate fastapi-deploy</code>
* Install the required python packages with <code>pip install -r src/requirements.txt</code> 

# 2. Folder structure
<pre>
.
├── .cfignore
├── .gitignore
├── README.md
├── docker-compose.yml
└── src
    ├── Dockerfile
    ├── Procfile
    ├── app
    │   ├── .env
    │   ├── .env_sample
    │   ├── __init__.py
    │   ├── dependencies.py
    │   ├── main.py
    │   └── routers
    │       ├── __init__.py
    │       └── sample.py
    ├── manifest.yml
    ├── requirements.txt
    ├── runtime.txt
    └── tests
        ├── __init__.py
        ├── conftest.py
        └── test_sample.py
</pre>
The purpose of the folders and files are summarized in the following sections.

## a. Procfile, manifest.yml runtime.txt .cfignore
These are the configurattion files needed for deployment to cloud foundry platform such as IBM Cloud Foundry. Review and change accordingly before deploy to cloud foundry platform. .cfignore file contain file that do not want to be uploaded to cloud foundry.

## b. docker-compose.yml
This is the config file for docker compose.

## c. .gitignore
Usually the .env manifest.yml ... etc files usually contain all the environment variables for the application.  If the environment variable included credentials / secret keys ... etc, it **should not** be check in to the git. For production, usually there are other way to set the eenvironment. Eg:
* cloud foundry: environment variables can be setup through console or the manifest.yml. 

## d. .cfignore
This file contains all the filename that do not want to be uploaded to cloud foundry.

## e. tests
This is the directory for all the unit tests. Any additional test should be added as:
* test file with name start or end with test_. Eg: test_1.py, 2_test.py
* test method's name must start with test. Eg:  
def testendpoint(...)

Unit test can be initiated with
<code>py.test -v</code>

# 3. Test Driven Development

* Create unit test file and method in src/tests directory.
* Run unit test with <code>py.test -v</code> and test should fail.
* Fix the unit test by adding code to main.py or routers/xxxx.py and rerun the unit test and make sure it pass.
* Refractor the code if neccessary.

# 4. Deployment - Local
* Unlike Django or Flask, FastAPI does not have a built-in development server. So, we'll use Uvicorn, an ASGI server, to serve up FastAPI.
* You can read more about ASGI from [Introduction to ASGI: Emergence of an Async Python Web Ecosystem](https://florimond.dev/blog/articles/2019/08/introduction-to-asgi-async-python-web/) blog post.
* Make sure FastAPI and Uvicorn are the requirements file.
* You can serve the FastAPI using either one of the following command: 
  *  <code>uvicorn src.app.main:app --reload</code>
  *  <code>uvicorn src.app.main:app --host=0.0.0.0 --port=${PORT:-5000}</code>
* Test the FASTAPI local deployment with:
  * http://localhost:5000/ping on browser, it should return {"ping": "pong!"}
  * OpenAPI based documentation can be view on browser from: http://localhost:5000/docs

# 5. Deployment - IBM cloud foundry

* Ensure the app completed all the unit & moudle tests without error.
* ensure that ibm cloud foundry deployment artifact **manifest.yml** are correctly specify with app name 
* ensure that ibm cloud foundry python deployment artifact **Procfile** are correctly specify with proper command
   * ensure that the app is running fine with command from **Procfile** locally, Eg. <code>uvicorn src.app.main:app --host=0.0.0.0 --port=${PORT:-5000}</code>
* login to IBM cloud foundry with <code>ibmcloud login --sso</code> 
* target IBM cloud foundry deployment to proper space, resource group... etc. with <code>ibmcloud target --cf</code>
* change directory to src with <code>cd src</code>
* deploy IBM cloud foundry with <code>ibmcloud cf push</code>
* if deployment failed, check the log file with <code>ibmcloud cf logs appname --recent</code> 
* Check the IBM cloud foundry app status with <code>ibmcloud cf app appname</code>, ensure that app with **running** status  
* Access the documentation of the API from route of the app under **https://routes/docs** from the status above with a browser

# 6. Deployment - docker local
* ensure that the app is running fine with uvicorn command locally.
* ensure that docker is installed locally.
* Review the sample **DockerFile** setup as follows:
  * Alpine-based Docker image for Python 3.8.1. 
  * set working directory
  * set two environment variables:
	  1. PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
	  2. PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
  * copy requirements file to proper directory
  * setup and install all the dependencies 
  * copy all the config and source code for the FASTAPI app
* Review the sample **docker-compose.yml** file
* Refer to [Docker for Python Developers](https://mherman.org/presentations/dockercon-2018/#1) for more details on docker
* Refer to [Compose file reference](https://docs.docker.com/compose/compose-file/) for more details on docker-compose
* The uvicorn will run with the following settings in docker container:
  * app.main:app tells Uvicorn where it can find the FastAPI ASGI application    
    *  e.g., "within the 'app' module, you'll find the ASGI app, app = FastAPI(), in the 'main.py' file.
  * --reload: enables auto-reload so the server will restart after changes are made to the code base.
  * --workers 1: provides a single worker process.
	* --host 0.0.0.0: defines the address to host the server on.
	* --port 8000: defines the port to host the server on.
* Refer to [Uvicorn setting](https://www.uvicorn.org/settings/) for more details about uvicorn setting.
* Build and run the docker container locally with either on of the following:
  * docker-compose: <code>docker-compose up -d --build</code>
  * docker: 
    * change directory to src with <code>cd src</code>
    * build docker image with <code>docker build -t yourusername/fastapi-sample .</code>
    * check docker images with <code>docker images</code>
    * Run the docker image with <code>docker run -d -p8002:8000  yourusername/fastapi-sample</code>
* Test the FASTAPI local docker deployment with:
  * http://localhost:8002/ping on browser, it should return {"ping": "pong!"}
  * OpenAPI based documentation can be view on browser from: http://localhost:8002/docs

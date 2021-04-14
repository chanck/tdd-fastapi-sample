'''
################################################################
# Below Example code show how to define schema to be used in the 
# respective url and method 
################################################################
class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

class Login(BaseModel):
    username: str = Form(...)
    password: str = Form(...)
################################################################
'''


'''
################################################################
# Below example code show to direct method for url /items/
################################################################
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.post("/items/")
async def update_item(item: Item):
    return item
################################################################

################################################################
# Below example code show to direct method for using form in url /login/
################################################################
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
#async def login(login:Login):
    return {"username": username}
################################################################

################################################################
# Below code show to direct method for using file upload 
################################################################
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
################################################################
'''

'''
################################################################
# Below code show how to use router for items, users 
################################################################
from .routers import items, users
from .internal import admin
from .dependencies import get_query_token, get_token_header

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
################################################################

################################################################
# Below code customize the default openapi schema 
################################################################

from fastapi.openapi.utils import get_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
################################################################
'''

from fastapi import FastAPI, Form, File, UploadFile, Request, Depends, Response, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional
from .routers import sample
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.include_router(sample.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI sample",
        version="0.1",
        description="This is the sample API for FastAPI framework.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

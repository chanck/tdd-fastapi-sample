'''
If you need some dependencies used in several places of the application.
So we put them in this dependencies module (app/dependencies.py).

For example:
Code below use a simple dependency to read a custom X-Token header:
##########################################################################
from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
##########################################################################
'''
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
import os

API_KEY = os.getenv("API_KEY") or "qwerasdf1234"
API_KEY_NAME = os.getenv("API_KEY_NAME") or "X-API-KEY" 

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def check_api_key(x_api_key: str = Security(api_key_header_auth)):
    """ takes the X-API-Key header and converts it into the matching user object from the database """

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

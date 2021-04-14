'''
###########################################################
# Below code show how to use router to define the items 
###########################################################

from fastapi import APIRouter, Depends, HTTPException, status

# if there are deependencies that needed in this moudle from common dependencies librabry
#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@router.put(
    "/{item_id}",
    tags=["custom"],
    response_model=Item,                            ## declare the model used for the response with the parameter 
    response_model_include={"name", "description"}, ## declare attributes included in response_model
    response_model_exclude={"tax"},                 ## declare attributes included in response_model
    responses={**responses, 401: {"description": "Authentication required"}},   ## **responses to include the responses dict
    status_code=status.HTTP_201_CREATED,            ## return status code 201
    summary="Create an item",                       ## change the default openai summary
    include_in_schema=False                         ## this is to exclude from OpenAPI documentation
)
async def update_item(item_id: str):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

###########################################################
'''

from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic import BaseModel, Field
from typing import Optional
# from ..dependencies import check_api_key   ## global dependency

router = APIRouter(
    prefix="/ping",
    tags=["ping"],
    # dependencies=[Security(check_api_key)],     ## make X-API-KEY global requirements
    responses={
        404: {"description": "Not found"},
        403: {"description": "Not authenticated, set your X-API-KEY headers to correct apiKey"}}
)

#@router.get("/",dependencies=[Security(check_api_key)]) 
@router.get("/",include_in_schema=True)    ## if include_in_schema set to false, the API will not show up in /docs
async def ping():
    """
    This is the sample ping endpoint
    - **name**: Sample ping
    - **description**: Sample ping long description
    - **parameter 1**: required
    \f
    :param item: User input.
    """
    return {"ping":"pong!"}
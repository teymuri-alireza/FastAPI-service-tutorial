"""
This file contains tutorial code for the FastAPI service course.
For the project codes check the branches starting with `project/*`.
"""

from fastapi import FastAPI, Query, status, HTTPException, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi_swagger import patch_fastapi
from contextlib import asynccontextmanager
from random import randint

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting")
    yield
    print("stoping")

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None, lifespan=lifespan)
patch_fastapi(app, redirect_from_root_to_docs=False)

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "maryam"},
    {"id": 3, "name": "navid"},
    {"id": 4, "name": "ehsan"},
    {"id": 5, "name": "sara"},
]

class NameList:
    def __init__(self, name):
        self.name = name

    def create_obj(self):
        new_obj = {"id": randint(10, 1000), "name": self.name}
        names_list.append(new_obj)

@app.get("/")
async def root():
    return {"response": "Hello World"}

@app.get("/names", status_code=status.HTTP_200_OK)
# async def list_names(search: str | None = None):
# async def list_names(search: Annotated[str | None, Query(max_length=25)] = None):
async def list_names(search: str | None = Query(default=None, max_length=25)):
    if search is not None:
        for item in names_list:
            if item["name"] == search:
                return item
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found"
        )
    else:
        content = {"repsonse": names_list}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@app.get("/names/{name_id}", status_code=status.HTTP_200_OK)
async def fetch_name(name_id: int):
    index = name_id - 1
    try:
        return {"response": names_list[index]}
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found"
        )

@app.post("/names", status_code=status.HTTP_201_CREATED)
# def create_name(
#     new_name: str = Query(examples=["John", "Marry"], min_length=3, max_length=30),
# ):
# def create_name(new_name: str = Body(), age: int = Body()):
def create_name(new_name: str = Form()):
    if new_name.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Name can't be digit",
        )
    instance = NameList(new_name)
    instance.create_obj()
    return new_name

@app.put("/names/{uid}", status_code=status.HTTP_200_OK)
def update_name(uid: int, new_name: str):
    index = uid - 1
    try:
        names_list[index]["name"] = new_name
        return new_name
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found"
        )

@app.delete("/names/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(uid: int):
    index = uid - 1
    try:
        del names_list[index]
        return {"reponse": "item deleted successfully"}
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found"
        )

@app.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile):
    # content = await file.read()
    return {
        "filename": file.filename,
        "content type": file.content_type,
        "size": file.size,
    }

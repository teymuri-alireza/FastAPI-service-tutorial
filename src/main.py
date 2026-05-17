from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, redirect_from_root_to_docs=False)

@app.get("/")
async def root():
    return {"response": "Hello World"}

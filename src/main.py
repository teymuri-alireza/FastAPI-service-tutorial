from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, redirect_from_root_to_docs=False)

@app.get("/")
async def root():
    return {"response": "Hello World"}

expenses_db = [
    {"id": 1, "description": "buy food", "amount": 12.45},
    {"id": 2, "description": "phone bill", "amount": 18.75},
    {"id": 3, "description": "pay tuition", "amount": 225.00},
    {"id": 4, "description": "buy hat", "amount": 48.99},
    {"id": 5, "description": "repair charger", "amount": 55.50},
]

from fastapi import FastAPI, status, Query, HTTPException, Form, Path
from fastapi.responses import JSONResponse
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

class Expense:
    """
    Represent an expense model.
    """
    def __init__(self, description: str, amount: float) -> None:
        """
        initialize the expense model.
        """
        self.description = description
        self.amount = amount
    
    def insert(self) -> int:
        """
        Calculate the new index and add the new expense to the database.

        Returns:
            int: Index of the new created item.
        """
        new_id = expenses_db[-1]["id"] + 1
        new_expense = {
            "id": new_id,
            "description": self.description,
            "amount": self.amount,
        }
        expenses_db.append(new_expense)

        new_index = new_id - 1
        return new_index

@app.get("/expenses")
async def list_expenses(item_id: int | None = Query(default=None, alias="id")):
    if item_id is not None:
        try:
            index = item_id - 1
            content = {"search result": expenses_db[index]}
            return JSONResponse(content=content, status_code=status.HTTP_200_OK)
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    else:
        content = {"expenses": expenses_db}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)

@app.post("/expenses", status_code=status.HTTP_201_CREATED)
async def add_expense(desc: str = Form(alias="description"), amount: float = Form(...)):
    new_expense = Expense(description=desc, amount=amount)
    index = new_expense.insert()
    return expenses_db[index]

@app.put("/expense/edit/{item_id}")
async def edit_expense(
    item_id: int = Path(),
    desc: str | None = Query(default=None, alias="description"),
    amount: float | None = Query(default=None)
    ):
    try:
        index = item_id - 1
        if desc is None and amount is None:
            content = {"status": "description and amount fields are empty. Nothing to change."}
            return JSONResponse(content=content, status_code=status.HTTP_200_OK)
        if desc is not None:
            if desc.isdigit():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="description can't be digit")
            else:
                expenses_db[index]["description"] = desc
        if amount is not None:
            expenses_db[index]["amount"] = amount
        content = {"status": "item updated successfully"}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

@app.delete("/expense/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(item_id: int = Path()):
    try:
        index = item_id - 1
        del expenses_db[index]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

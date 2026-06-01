from fastapi import FastAPI, status, Query, HTTPException, Path
from fastapi_swagger import patch_fastapi
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema

# Use patch_fastapi() to load swagger UI faster
app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, redirect_from_root_to_docs=False)

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

    def insert(self) -> int | None:
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

        new_index = find_expense_index(new_id)
        return new_index


def find_expense_index(item_id) -> int | None:
    """
    Find an item's index using item's id value with a for loop.
    Otherwise return `None`.
    """
    for item in expenses_db:
        if item["id"] == item_id:
            return expenses_db.index(item)
    return None


@app.get("/expenses", response_model=ExpenseResponseSchema | list[ExpenseResponseSchema])
async def list_expenses(item_id: int | None = Query(default=None, alias="id")):
    if item_id is not None:
        # Search for an expense with a given ID
        try:
            index = find_expense_index(item_id)
            if index is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
            return expenses_db[index]
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    else:
        return expenses_db


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseResponseSchema)
async def add_expense(expense: ExpenseCreateSchema):
    new_expense = Expense(description=expense.description, amount=expense.amount)
    index = new_expense.insert()
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return expenses_db[index]


@app.put("/expense/edit/{item_id}", response_model=ExpenseResponseSchema)
async def edit_expense(
    expense: ExpenseUpdateSchema,
    item_id: int = Path(),
    ):
    try:
        index = find_expense_index(item_id)
        if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
        # If no new values are provided
        if expense.description is None and expense.amount is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
        if expense.description is not None:
            if expense.description.isdigit():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="description can't be digit")
            else:
                # Update description value
                expenses_db[index]["description"] = expense.description
        if expense.amount is not None:
            # update amount value
            expenses_db[index]["amount"] = expense.amount
        return expenses_db[index]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")


@app.delete("/expense/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(item_id: int = Path()):
    try:
        index = find_expense_index(item_id)
        if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
        del expenses_db[index]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

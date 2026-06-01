from pydantic import BaseModel, Field, field_serializer


class ExpenseBaseModel(BaseModel):
    """
    Base model for expense entities.

    Attributes:
        description (str): Description of the expense.
        amount (float): Cost of the expense.

    **Serialization:**
        The `amount` field is rounded to two decimal places during serialization.
    """
    description: str = Field(..., description="Description of the expense.")
    amount: float = Field(..., description="Cost of the expense.")

    @field_serializer("amount")
    def round_amount(self, amount: float):
        return round(amount, 2)

class ExpenseResponseSchema(ExpenseBaseModel):
    """
    Represents an expense returned by the API.

    Attributes:
        id (int): Unique identifier of the expense.
    """
    id: int = Field(..., description="Unique identifier of the expense.")

class ExpenseCreateSchema(ExpenseBaseModel):
    """
    Represents the payload required to create a new expense.
    """
    pass

class ExpenseUpdateSchema(BaseModel):
    """
    Represents a partial expense update request.

    Attributes:
        description (str|None): Updated expense description.
        amount (float|None): Updated expense amount.
    """
    description: str | None = None
    amount: float | None = None

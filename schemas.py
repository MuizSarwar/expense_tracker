from pydantic import BaseModel,EmailStr, Field, field_validator
from datetime import date as date_type
from typing import Optional







#--------------------------------------------------------------------------------------------------------------------
# Schema to Create a valid User  
#--------------------------------------------------------------------------------------------------------------------

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str






#--------------------------------------------------------------------------------------------------------------------
# Schema to Create a valid Expense  
#--------------------------------------------------------------------------------------------------------------------

class CreateExpense(BaseModel):
    title: str
    amount: float = Field(..., gt=0, description="Must be a positive number")
    type: str
    category: str
    date: date_type

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("income", "expense"):
            raise ValueError('type must be either "income" or "expense"')
        return v





#--------------------------------------------------------------------------------------------------------------------
# Schema to Update a Expense
#--------------------------------------------------------------------------------------------------------------------

class UpdateExpense(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date_type] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("income", "expense"):
            raise ValueError('type must be either "income" or "expense"')
        return v





#--------------------------------------------------------------------------------------------------------------------
# Schema to response data  
#--------------------------------------------------------------------------------------------------------------------

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date_type
    owner_id: int

    class Config:
        from_attributes = True  
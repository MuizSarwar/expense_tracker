from fastapi import APIRouter, HTTPException, Depends, Path, Query, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional, Literal

from database import get_db
from models import User, Transaction
from schemas import CreateExpense, UpdateExpense, TransactionResponse
from security import get_current_user




router = APIRouter(
    prefix="/transactions",
    tags=["Transaction CRUD Operations"]
)




#--------------------------------------------------------------------------------------------------------------------
# Dependencies
#--------------------------------------------------------------------------------------------------------------------
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]








#--------------------------------------------------------------------------------------------------------------------
# API routers
#--------------------------------------------------------------------------------------------------------------------


@router.post('', response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transactions(db: db_dependency, current_user: user_dependency, new_transaction: CreateExpense):
    transaction_model = Transaction(
        title=new_transaction.title,
        amount=new_transaction.amount,
        type=new_transaction.type,
        category=new_transaction.category,
        date=new_transaction.date,
        owner_id=current_user.id,
    )
    db.add(transaction_model)
    db.commit()
    db.refresh(transaction_model)
    return transaction_model





@router.get('', response_model=list[TransactionResponse])
async def get_all_transactions(db: db_dependency, current_user: user_dependency):
    return db.query(Transaction).filter(Transaction.owner_id == current_user.id).all()






@router.get('/filter', response_model=list[TransactionResponse])
async def filter_transactions(
    db: db_dependency,
    current_user: user_dependency,
    type: Optional[Literal["expense", "income"]] = Query(default=None, description="Filter by transaction type"),
    category: Optional[str] = Query(default=None, description="Filter by category, e.g. 'Food'"),
    minimum_amount: Optional[float] = Query(default=None, ge=0, description="Minimum amount (inclusive)"),
    maximum_amount: Optional[float] = Query(default=None, ge=0, description="Maximum amount (inclusive)"),
):
    query = db.query(Transaction).filter(Transaction.owner_id == current_user.id)

    if type is not None:
        query = query.filter(Transaction.type == type)
    if category is not None:
        query = query.filter(Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(Transaction.amount <= maximum_amount)

    return query.all()






@router.get('/{transaction_id}', response_model=TransactionResponse)
async def get_transactions_by_id(
    db: db_dependency,
    current_user: user_dependency,
    transaction_id: Annotated[int, Path(gt=0, description="Id number for each transaction")],
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction







@router.put('/{transaction_id}', response_model=TransactionResponse)
async def update_transactions_by_id(
    db: db_dependency,
    current_user: user_dependency,
    updated_data: UpdateExpense,
    transaction_id: Annotated[int, Path(gt=0)],
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    update_fields = updated_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction








@router.delete('/{transaction_id}')
async def delete_transactions_by_id(
    db: db_dependency,
    current_user: user_dependency,
    transaction_id: Annotated[int, Path(gt=0)],
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
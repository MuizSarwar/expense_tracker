from fastapi import FastAPI, HTTPException, Depends, Path, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import date

from database import Base, engine, get_db
from models import User, Transaction
from routers import auth
from schemas import CreateExpense, UpdateExpense, TransactionResponse
from security import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)






#--------------------------------------------------------------------------------------------------------------------
# Dependencies
#--------------------------------------------------------------------------------------------------------------------
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]








#--------------------------------------------------------------------------------------------------------------------
# API routers
#--------------------------------------------------------------------------------------------------------------------

@app.post('/transactions', response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
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






@app.get('/transactions', response_model=list[TransactionResponse])
async def get_all_transactions(db: db_dependency, current_user: user_dependency):
    return db.query(Transaction).filter(Transaction.owner_id == current_user.id).all()







@app.get('/transactions/{transaction_id}', response_model=TransactionResponse)
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






@app.put('/transactions/{transaction_id}', response_model=TransactionResponse)
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







@app.delete('/transactions/{transaction_id}')
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
from fastapi import FastAPI, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated

from database import Base, engine, get_db
import models
from routers import auth


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)





#--------------------------------------------------------------------------------------------------------------------
# Dependency
#--------------------------------------------------------------------------------------------------------------------
db_dependency = Annotated[Session, Depends(get_db)]







#--------------------------------------------------------------------------------------------------------------------
# API routers
#--------------------------------------------------------------------------------------------------------------------
@app.post('/transactions')
async def create_transactions(db: db_dependency):
    pass


@app.get('/transactions')
async def get_all_transactions(db: db_dependency):
    pass


@app.get('/transactions/{transaction_id}')
async def get_transactions_by_id(
    db: db_dependency,
    transaction_id: Annotated[int, Path(gt=100, description="Id number for each transaction", examples=[101])],
):
    pass


@app.put('/transactions/{transaction_id}')
async def update_transactions_by_id():
    pass


@app.delete('/transactions/{transaction_id}')
async def delete_transactions_by_id():
    pass
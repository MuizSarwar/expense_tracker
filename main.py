from fastapi import FastAPI

from database import Base, engine
from routers import auth, transactions

app = FastAPI()

Base.metadata.create_all(bind=engine)






#--------------------------------------------------------------------------------------------------------------------
# API routers
#--------------------------------------------------------------------------------------------------------------------


app.include_router(auth.router)
app.include_router(transactions.router)
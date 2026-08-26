from pydantic import BaseModel, EmailStr






#--------------------------------------------------------------------------------------------------------------------
# Schema to Create a valid User  
#--------------------------------------------------------------------------------------------------------------------

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str








from pydantic import BaseModel, EmailStr

class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr  # Use Pydantic's EmailStr for email validation
    # ... other fields ...

    class Config:
        orm_mode = True  # If using an ORM like SQLAlchemy

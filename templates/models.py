from pydantic import BaseModel, Field

class Item(BaseModel):
    creator : str = Field(min_length=1)
    model : str = Field(min_length=1)
    price : int = Field(ge=0)
    category :str = Field(min_length=1)


class UserLogin(BaseModel):
    username: str = Field(min_length=1) # минимальное значение символов 1
    password: str = Field(min_length = 8)# минимальное значение символов 8
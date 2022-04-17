

from pydantic import BaseModel


class BaseView(BaseModel):
    class Config:
        orm_mode = True

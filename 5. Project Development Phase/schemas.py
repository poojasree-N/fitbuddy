from pydantic import BaseModel


class UserInput(BaseModel):
    name: str
    age: int
    weight: float
    goal: str
    intensity: str
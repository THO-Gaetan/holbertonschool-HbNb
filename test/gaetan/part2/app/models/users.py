from app.models.basemodel import BaseModel

class user(BaseModel):
    def __init__(self, name, email):
        super().__init__()
        self.name = name
        self.email = email
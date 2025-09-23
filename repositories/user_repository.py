from sqlmodel import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

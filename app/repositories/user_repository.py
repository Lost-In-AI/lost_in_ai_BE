from sqlmodel import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user):
        try:
            self.db.add(user)
            self.db.commit()
        except Exception as e:
            raise e

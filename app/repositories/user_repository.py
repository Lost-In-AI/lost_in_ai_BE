from sqlmodel import Session, select

from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_user_by_id(self, user_id = str):
        try:
            statement = select(User).where(User.user_id == user_id)
            return self.db.exec(statement).one_or_none()
        except Exception as e:
            raise Exception(f"Error getting user by user_id {user_id}. Error: {e}")


    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return None

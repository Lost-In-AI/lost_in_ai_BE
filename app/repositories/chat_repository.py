from sqlmodel import Session as SQLSession, select
from uuid import UUID

from models.session import Session as SessionModel
from models.message import Message


class ChatRepository:
    def __init__(self, db: SQLSession):
        self.db = db


    def create_session(self, session: SessionModel) -> SQLSession:
        try:
            self.db.add(session)
            self.db.flush()
            self.db.refresh(session)
            return session
        except Exception as e:
            raise Exception(f"Error saving session with session_id {session.session_id}. Error: {e}")

    def create_message(self, message: Message) -> Message:
        try:
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message
        except Exception as e:
            raise Exception(f"Error saving message. Error: {e}")

    def get_session_messages(self, session_id: UUID):
        try:
            statement = select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
            return self.db.exec(statement).all()
        except Exception as e:
            raise Exception(f"Error getting messages for session_id {session_id}. Error: {e}")


    def get_session(self, session_id: str):
        try:
            statement = select(SessionModel).where(SessionModel.session_id == session_id)
            return self.db.exec(statement).all()
        except Exception as e:
            raise e

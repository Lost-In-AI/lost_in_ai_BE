from models.user import User


class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository


    def create_user(self, event_payload: dict):
        user = User(
            id=event_payload.get('id'),
            email=event_payload.get('email_addresses')[0]['email_address'],
            name=event_payload.get('unsafe_metadata')['firstName'],
            surname=event_payload.get('unsafe_metadata')['LastName'],
        )

        self.user_repository.create_user(user)
        self.user_repository.db.commit()

        return None

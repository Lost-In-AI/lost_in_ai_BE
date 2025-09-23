from models.user import User


class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository


    def create_user(self, event_payload: dict):
        user = User(
            user_id=event_payload.get('id'),
            name=event_payload.get('first_name'),
            surname=event_payload.get('last_name'),
            email=event_payload.get('email_addresses')[0]['email_address'],
            cf=event_payload.get('unsafe_metadata')['cf'],
            address=event_payload.get('unsafe_metadata')['address'],
            phone=event_payload.get('unsafe_metadata')['phone'],
            status='active',
            password='00000000',
            role_id=2
        )

        self.user_repository.create_user(user)
        self.user_repository.db.commit()

        return None

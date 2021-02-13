from api.db import session_scope


class Storage:

    @staticmethod
    def save_message(user_name, message_text):
        from api.db.models import Message, User
        with session_scope() as s:
            user = s.query(User).filter(User.nickname == user_name).first()
            if not user:
                user = User(nickname=user_name)
            s.add(
                Message(
                    text=message_text,
                    user=user
                )
            )

    @staticmethod
    def get_data():
        class InnerMessage:
            def __init__(self, text, create_at, user_name):
                self.text = text
                self.create_at = create_at
                self.user_name = user_name

        messages = []
        from api.db.models import Message
        with session_scope() as s:
            data = s.query(Message).all()
            for item in data:
                messages.append(
                    InnerMessage(
                        item.text,
                        item.create_at,
                        item.user.nickname
                    )
                )
            return messages

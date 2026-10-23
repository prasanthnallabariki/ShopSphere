from accounts.repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def register_user(validated_data):
        return UserRepository.create_user(validated_data)
        
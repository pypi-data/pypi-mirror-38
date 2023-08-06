class User:
    """
    Модель для пользователя карты
    """
    def __init__(self, id, username, name, surname, role):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.role = role

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"
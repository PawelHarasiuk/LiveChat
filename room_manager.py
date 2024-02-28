import random
from string import ascii_uppercase


class RoomManager:
    def __init__(self, app):
        self.app = app
        self.rooms = {}

    def generate_unique_code(self, length):
        while True:
            code = "".join(random.choice(ascii_uppercase) for _ in range(length))
            if code not in self.rooms:
                break
        return code

    def create_room(self, length=4):
        room_code = self.generate_unique_code(length)
        self.rooms[room_code] = {"members": 0, "messages": []}
        return room_code

    def get_room(self, code):
        return self.rooms.get(code)

    def remove_room(self, code):
        if code in self.rooms:
            del self.rooms[code]

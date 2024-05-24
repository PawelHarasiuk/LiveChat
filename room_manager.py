import random
from string import ascii_uppercase


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def generate_unique_code(self, length):
        while True:
            code = "".join(random.choices(ascii_uppercase, k=length))
            if code not in self.rooms:
                return code

    def create_room(self):
        code = self.generate_unique_code(4)
        self.rooms[code] = {"members": 0, "messages": []}
        return code

    def join_room(self, code):
        if code not in self.rooms:
            return False
        return True

    def leave_room(self, code):
        if code in self.rooms:
            del self.rooms[code]
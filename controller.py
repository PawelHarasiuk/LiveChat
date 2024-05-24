from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from room_manager import RoomManager


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "passwd"
        self.socketio = SocketIO(self.app)
        self.room_manager = RoomManager()

        self.configure_routes()
        self.configure_sockets()

    def run(self):
        self.socketio.run(self.app, debug=False, allow_unsafe_werkzeug=True, port=5000)

    def configure_routes(self):
        @self.app.route("/", methods=["POST", "GET"])
        def home():
            session.clear()
            if request.method == "POST":
                name = request.form.get("name")
                code = request.form.get("code")
                join = request.form.get("join", False)
                create = request.form.get("create", False)

                if not name:
                    return render_template("home.html", error="Please enter a name.", code=code, name=name)

                if join != False and not code:
                    return render_template("home.html", error="Please enter a room code.", code=code, name=name)

                room = code
                if create != False:
                    room = self.room_manager.generate_unique_code(4)
                    self.room_manager.rooms[room] = {"members": 0, "messages": []}
                elif code not in self.room_manager.rooms:
                    return render_template("home.html", error="Room does not exist.", code=code, name=name)

                session["room"] = room
                session["name"] = name
                return redirect(url_for("room"))

            return render_template("home.html")

        @self.app.route("/room")
        def room():
            room_code = session.get("room")
            if room_code is None or session.get("name") is None:
                return redirect(url_for("home"))

            room_data = self.room_manager.rooms.get(room_code)
            if room_data is None:
                return redirect(url_for("home"))

            return render_template("room.html", code=room_code, messages=room_data["messages"])

    def configure_sockets(self):
        @self.socketio.on("message")
        def message(data):
            room_code = session.get("room")
            if room_code is not None:
                content = {"name": session.get("name"), "message": data["data"]}
                send(content, to=room_code)
                self.room_manager.rooms[room_code]["messages"].append(content)
                print(f"{session.get('name')} said: {data['data']}")

        @self.socketio.on("connect")
        def connect(auth):
            room_code = session.get("room")
            name = session.get("name")
            if room_code is not None and name is not None:
                join_room(room_code)
                send({"name": name, "message": "has entered the room"}, to=room_code)
                self.room_manager.rooms[room_code]["members"] += 1
                print(f"{name} joined room {room_code}")

        @self.socketio.on("disconnect")
        def disconnect():
            room_code = session.get("room")
            name = session.get("name")
            if room_code is not None and name is not None:
                leave_room(room_code)
                if room_code in self.room_manager.rooms:
                    self.room_manager.rooms[room_code]["members"] -= 1
                    if self.room_manager.rooms[room_code]["members"] <= 0:
                        del self.room_manager.rooms[room_code]
                send({"name": name, "message": "has left the room"}, to=room_code)
                print(f"{name} has left the room {room_code}")
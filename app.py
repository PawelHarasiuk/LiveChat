from flask import Flask, request, render_template, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from room_manager import RoomManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"
socketio = SocketIO(app)
room_manager = RoomManager(app)


@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create:
            room = room_manager.create_room()
        elif code not in room_manager.rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    room_code = session.get("room")
    if room_code is None or session.get("name") is None or room_code not in room_manager.rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room_code, messages=room_manager.get_room(room_code)["messages"])


@socketio.on("message")
def message(data):
    room_code = session.get("room")
    if room_code not in room_manager.rooms:
        return

    content = {"name": session.get("name"), "message": data["data"]}
    send(content, to=room_code)
    room_manager.get_room(room_code)["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room_code = session.get("room")
    name = session.get("name")
    if not room_code or not name:
        return
    if room_code not in room_manager.rooms:
        leave_room(room_code)
        return

    join_room(room_code)
    send({"name": name, "message": "has entered the room"}, to=room_code)
    room_manager.get_room(room_code)["members"] += 1
    print(f"{name} joined room {room_code}")


@socketio.on("disconnect")
def disconnect():
    room_code = session.get("room")
    name = session.get("name")
    leave_room(room_code)

    if room_code in room_manager.rooms:
        room_manager.get_room(room_code)["members"] -= 1
        if room_manager.get_room(room_code)["members"] <= 0:
            room_manager.remove_room(room_code)

    send({"name": name, "message": "has left the room"}, to=room_code)
    print(f"{name} has left the room {room_code}")


if __name__ == "__main__":
    socketio.run(app, debug=True)

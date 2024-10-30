# Chat Application

This is a chat application developed using Flask and Flask-SocketIO. It allows users to create and join chat rooms where they can exchange messages in real-time.


## Features
- **Create and Join Rooms:** Users can create new chat rooms or join existing ones by entering a room code.
- **Real-time Messaging:** Messages are delivered instantly to all participants in a room.
- **Dynamic User Count:** The application keeps track of the number of users in each room and updates it in real-time.
- **Simple Interface:** The user interface is designed to be intuitive and easy to use.
  
<img width="1225" alt="Zrzut ekranu 2024-05-25 o 01 11 06" src="https://github.com/PawelHarasiuk/LiveChat/assets/96013656/eab3c495-faa0-4826-a973-ea0fb2556fd6">

## Usage
1. **Home Page:**
   - Upon visiting the application, users are directed to the home page where they can enter their name and choose to join an existing room or create a new one.
   - If creating a new room, a unique room code is generated automatically.
   
2. **Chat Room:**
   - Once inside a chat room, users can exchange messages with other participants.
   - Messages are displayed in real-time as they are sent.
   - Users receive notifications when others join or leave the room.

## Implementation Details
- The application is built using the Flask web framework for the backend.
- Flask-SocketIO is used to enable real-time communication between the server and clients.
- User sessions are managed using Flask's session management.
- Room management functionality is implemented in the `RoomManager` class.

## Dependencies
- Flask
- Flask-SocketIO

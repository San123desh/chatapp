# FastAPI Chat Application

A real-time chat application built with FastAPI, WebSockets, and PostgreSQL featuring JWT authentication and role-based access control.

## Project Overview


### Group A 

#### 1. Environment & Dependencies
- **Virtual Environment**: Set up using `python3 -m venv venv` for isolated project dependencies
- **Essential Packages**: 
  - FastAPI (web framework)
  - Uvicorn (ASGI server)
  - SQLModel (ORM for PostgreSQL)
  - psycopg2 (PostgreSQL adapter)
  - passlib (password hashing)
  - python-jose (JWT handling)

#### 2. JWT Authentication & Role-Based Access Control (RBAC)
- **User Model**: SQLModel model with role field categorizing users as `admin` or `user`
- **Authentication Endpoints**:
  - `POST /auth/signup`: Accepts user credentials, hashes password, stores user with assigned role
  - `POST /auth/login`: Verifies credentials, generates JWT token signed with HS256, embedding user's role
- **RBAC Dependency**: Reusable dependency to restrict access to routes based on user's role

#### 3. Protected WebSocket Chat
- **WebSocket Endpoint**: `/ws/{room_name}` route in FastAPI to handle WebSocket connections
- **JWT Authentication**: Secures WebSocket connection by verifying JWT token passed as query parameter
- **Chat Functionality**:
  - On connection, fetches and sends recent messages from PostgreSQL using cursor-based pagination
  - Broadcasts incoming messages to all connected clients in the same room
  - Stores messages in the messages table

### Group B - Task 1: PostgreSQL Persistence ✅

#### Database Integration
- **ORM**: Utilizes SQLModel for ORM-based interaction with PostgreSQL
- **Models**:
  - **User**: Stores user information, including credentials and role
  - **Room**: Represents chat rooms with metadata (name, description)
  - **Message**: Captures individual messages, linking them to users and rooms, storing timestamps
- **Relationships**: Proper one-to-many relationships between Room and Message, User and Message

## 🏗️ Architecture

### Database Schema
```
User (id, username, email, hashed_password, role)
  ↓ (one-to-many)
Message (id, content, timestamp, user_id, room_id)
  ↑ (one-to-many)
Room (id, name, description, created_by)
```

### Key Features
- **Real-time messaging** via WebSockets
- **JWT-based authentication** with role-based access
- **Room-based chat** with admin-only rooms
- **Message persistence** in PostgreSQL
- **Recent message history** on connection
- **User join/leave notifications**

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### 1. Clone the repository
```bash
git clone https://github.com/San123desh/chatapp.git
cd chatapp
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure database
Create a PostgreSQL database and update `config/settings.py`:
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/chat_app"
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
```

### 5. Initialize database
```bash
python init_db.py
```

### 6. Create default rooms
```bash
python init_rooms.py
```

### 7. Start the server
```bash
uvicorn main:app --reload
```

## 📡 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### Room Management (Admin Only)
- `POST /rooms` - Create new room
- `DELETE /rooms/{room_name}` - Delete room

### Chat
- `GET /messages/{room_name}` - Get room messages
- `WS /ws/{room_name}` - WebSocket chat endpoint

## 🔧 Usage Examples

### 1. Create a user
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "password123",
    "role": "user"
  }'
```

### 2. Login and get token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "password123"
  }'
```

### 3. Connect to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/general?token=YOUR_JWT_TOKEN');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.send('Hello, everyone!');
```

## 🧪 Testing

### Run the test script
```bash
python test_ws.py
```

### Generate fresh tokens
```bash
python generate_tokens.py
```

## 📁 Project Structure
```
├── main.py                 # FastAPI application entry point
├── config/
│   └── settings.py        # Configuration settings
├── models/
│   ├── __init__.py        # Model imports
│   ├── user.py           # User model with roles
│   ├── room.py           # Room model
│   └── message.py        # Message model
├── routes/
│   ├── auth.py           # Authentication endpoints
│   └── chat.py           # WebSocket and room endpoints
├── dependencies/
│   └── auth.py           # JWT and RBAC dependencies
├── utils/
│   └── security.py       # Password hashing and JWT utilities
├── init_db.py            # Database initialization
├── init_rooms.py         # Default room creation
├── generate_tokens.py    # Token generation utility
└── test_ws.py           # WebSocket test script
```

## 🔐 Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with role-based claims
- **Role-Based Access**: Admin and user roles with different permissions
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLModel ORM prevents SQL injection

## 🎯 Key Implementation Details

### Group A Achievements
1. **Complete JWT Authentication**: Full signup/login flow with role embedding
2. **RBAC System**: `require_role` dependency for route protection
3. **WebSocket Security**: JWT verification for WebSocket connections
4. **Real-time Chat**: Live messaging with broadcasting

### Group B Achievements
1. **PostgreSQL Integration**: Full ORM-based database interaction
2. **Proper Relationships**: One-to-many relationships between all models
3. **Cursor-based Pagination**: Efficient message history retrieval
4. **Room Management**: Create/delete rooms with proper foreign key constraints

## 🚀 Future Enhancements

- [ ] Message encryption
- [ ] File sharing capabilities
- [ ] User presence indicators
- [ ] Message reactions
- [ ] Push notifications
- [ ] Mobile app integration

## 📄 License

This project is created for educational purposes and task completion.

---

**Built with ❤️ using FastAPI, SQLModel, and PostgreSQL**
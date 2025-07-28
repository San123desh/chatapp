from sqlmodel import Session, select
from models.room import Room
from models.user import User
from config.settings import settings
from sqlmodel import create_engine

def init_rooms():
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as session:
        # Check if default rooms exist
        general_room = session.exec(select(Room).where(Room.name == "general")).first()
        admin_room = session.exec(select(Room).where(Room.name == "admin_room")).first()
        
        # Get the first user (or create a default admin user)
        admin_user = session.exec(select(User).where(User.role == "admin")).first()
        if not admin_user:
            # If no admin user exists, get the first user
            admin_user = session.exec(select(User)).first()
        
        if not admin_user:
            print("No users found. Please create users first.")
            return
        
        # Create general room if it doesn't exist
        if not general_room:
            general_room = Room(
                name="general",
                description="General chat room for all users",
                created_by=admin_user.id
            )
            session.add(general_room)
            print("Created general room")
        
        # Create admin room if it doesn't exist
        if not admin_room:
            admin_room = Room(
                name="admin_room",
                description="Admin-only chat room",
                created_by=admin_user.id
            )
            session.add(admin_room)
            print("Created admin_room")
        
        session.commit()
        print("Room initialization completed!")

if __name__ == "__main__":
    init_rooms() 
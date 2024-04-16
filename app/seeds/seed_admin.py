from sqlalchemy.orm import sessionmaker
from app.config.database import Base, engine
from app.models.admin_model import User 

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

def user_seed_data():
    # Create dummy data for users
    user_data = [
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "hashed_password": "hashedpassword1",
            "roles": ["Admin"]
        },
        {
            "email": "jane.doe@example.com",
            "username": "janedoe",
            "hashed_password": "hashedpassword2",
            "roles": ["Admin"]
        },
    ]

    # Create and add user instances to the session
    for user in user_data:
        new_user = User(**user)
        session.add(new_user)
    
    # Commit the session to save the users to the database
    session.commit()

    print("Data seeded successfully!")
from app import app, db
from models import User


users = [
    {
        "email": "demo@usiug6.com",
        "password": "demo1234",
        "firstName": "Demo",
        "lastName": "User",
        "role": "admin"
    },
    {
        "email": "user1@example.com",
        "password": "password123",
        "firstName": "Jane",
        "lastName": "Doe",
        "role": "user"
    }
]

def seed_database():
    """Seed database"""
    users_data = users   
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        print("Starting database seeding...")
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            
            if existing_user:
                print(f"User {user_data['email']} already exists.")
                continue
            
            # Create new user
            new_user = User(
                first_name=user_data['firstName'],
                last_name=user_data['lastName'],
                email=user_data['email']
            )
            
            # Set password
            new_user.set_password(user_data['password'])
            
            # Add to database
            db.session.add(new_user)
            print(f"Created user: {user_data['email']} ({user_data['firstName']} {user_data['lastName']})")
        
        # Commit all changes
        db.session.commit()
        print("Database seeding completed!")
        
        # Show all users
        all_users = User.query.all()
        print(f"\nTotal users in database: {len(all_users)}")
        for user in all_users:
            print(f"   - {user.email} ({user.first_name} {user.last_name})")


if __name__ == '__main__':
    seed_database()

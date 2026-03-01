# create_db.py
from app import app, db

def create_database():
    with app.app_context():
        db.create_all()
        print("Успешно")
        return True

if __name__ == '__main__':
    create_database()
from app import create_app
from app.database import db
from app.seed_data import seed_diseases

app = create_app()

with app.app_context():
    db.create_all()
    seed_diseases(db.session)
    db.session.commit()

print("Database initialized and seeded.")

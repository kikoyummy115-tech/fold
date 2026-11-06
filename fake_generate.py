import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from werkzeug.security import generate_password_hash

# Import your Flask app and db instance
from extension import db
from app.models import User
from app import create_app

fake = Faker()


app = create_app()

TOTAL_RECORDS = 10000
CHUNK_SIZE = 2000
ROLE_ID = "9adec9a9-49e6-44b0-ac5b-6ec2e5ecad22"
GENDERS = ["male", "female", "other"]

def seed_users():
    with app.app_context():
        print(f"Preparing to generate {TOTAL_RECORDS} users...")

        # 1. Pre-hash password once so it doesn't slow down generation
        hashed_pw = generate_password_hash("11111111")
        
        users_batch = []
        used_emails = set()

        now = datetime.now(timezone.utc)

        for i in range(1, TOTAL_RECORDS + 1):
            # Generate a unique email
            email = fake.unique.email()

            # Optional fallback safeguard against collision
            while email in used_emails:
                email = f"{fake.user_name()}_{uuid.uuid4().hex[:6]}@{fake.free_email_domain()}"
            used_emails.add(email)

            gender = random.choice(GENDERS)
            dob = fake.date_of_birth(minimum_age=18, maximum_age=65)

            user_data = {
                "id": str(uuid.uuid4()),
                "username": fake.user_name()[:99],
                "email": email,
                "password_hash": hashed_pw,
                "role_id": ROLE_ID,
                "img_url": None,
                "gender": gender,
                "date_of_birth": dob,
                "last_seen": now,
                "created_at": now,
                "updated_at": now,
            }

            users_batch.append(user_data)

            # Insert in chunks to optimize memory and PostgreSQL connection buffer
            if len(users_batch) >= CHUNK_SIZE:
                db.session.bulk_insert_mappings(User, users_batch)
                db.session.commit()
                print(f"Inserted {i} / {TOTAL_RECORDS} users...")
                users_batch.clear()

        # Insert any remaining records
        if users_batch:
            db.session.bulk_insert_mappings(User, users_batch)
            db.session.commit()

        print(f"Successfully seeded {TOTAL_RECORDS} users!")

if __name__ == "__main__":
    seed_users()
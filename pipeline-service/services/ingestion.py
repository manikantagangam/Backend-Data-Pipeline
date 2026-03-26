import requests
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer

FLASK_BASE_URL = "http://mock-server:5000"

def fetch_all_customers():
    all_data = []
    page = 1
    limit = 10
    while True:
        resp = requests.get(f"{FLASK_BASE_URL}/api/customers", params={"page": page, "limit": limit})
        resp.raise_for_status()
        body = resp.json()
        all_data.extend(body["data"])
        if len(all_data) >= body["total"]:
            break
        page += 1
    return all_data

def upsert_customers(db: Session, customers: list):
    for c in customers:
        stmt = insert(Customer).values(
            customer_id=c["customer_id"],
            first_name=c["first_name"],
            last_name=c["last_name"],
            email=c["email"],
            phone=c.get("phone"),
            address=c.get("address"),
            date_of_birth=c.get("date_of_birth"),
            account_balance=c.get("account_balance"),
            created_at=c.get("created_at"),
        ).on_conflict_do_update(
            index_elements=["customer_id"],
            set_={
                "first_name": c["first_name"],
                "last_name": c["last_name"],
                "email": c["email"],
                "account_balance": c.get("account_balance"),
            }
        )
        db.execute(stmt)
    db.commit()
    return len(customers)
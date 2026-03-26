from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from models.customer import Customer
from services.ingestion import fetch_all_customers, upsert_customers

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.post("/api/ingest")
def ingest(db: Session = Depends(database.get_db)):
    try:
        customers = fetch_all_customers()
        count = upsert_customers(db, customers)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(database.get_db)):
    offset = (page - 1) * limit
    total = db.query(Customer).count()
    customers = db.query(Customer).offset(offset).limit(limit).all()
    return {
        "data": [c.__dict__ for c in customers],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(database.get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.__dict__
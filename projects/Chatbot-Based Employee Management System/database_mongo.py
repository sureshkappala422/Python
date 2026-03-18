from pymongo import MongoClient, ReturnDocument
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["employee_db"]
collection = db["employees"]
_counters = db["counters"]


def save_employee(data):
    collection.insert_one(data)
    return data


def find_employee_by_id(employee_id):
    return collection.find_one({"employee_id": employee_id}, {"_id": 0})


def list_employees(filters, skip, limit):
    cursor = collection.find(filters, {"_id": 0}).skip(skip).limit(limit)
    return list(cursor)


def count_employees(filters):
    return collection.count_documents(filters)


def update_employee(employee_id, updates):
    result = collection.update_one({"employee_id": employee_id}, {"$set": updates})
    if result.matched_count == 0:
        return None
    return find_employee_by_id(employee_id)


def delete_employee(employee_id):
    result = collection.delete_one({"employee_id": employee_id})
    return result.deleted_count > 0


def get_next_employee_id():
    doc = _counters.find_one_and_update(
        {"_id": "employee_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    seq = int(doc.get("seq", 1))
    return f"EMP{seq:06d}"

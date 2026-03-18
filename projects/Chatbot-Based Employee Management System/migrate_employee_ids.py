from pymongo import MongoClient
from config import MONGO_URI


def main():
    client = MongoClient(MONGO_URI)
    db = client["employee_db"]
    employees = db["employees"]
    counters = db["counters"]

    docs = list(employees.find({}, {"_id": 1}).sort("_id", 1))
    if not docs:
        print("No employees found.")
        return

    for index, doc in enumerate(docs, start=1):
        new_id = f"EMP{index:06d}"
        employees.update_one({"_id": doc["_id"]}, {"$set": {"employee_id": new_id}})

    counters.update_one(
        {"_id": "employee_id"},
        {"$set": {"seq": len(docs)}},
        upsert=True,
    )

    print(f"Updated {len(docs)} employees. Counter set to {len(docs)}.")


if __name__ == "__main__":
    main()

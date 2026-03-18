from datetime import datetime, timezone
from logger_config import logger
from database_mongo import get_next_employee_id


def generate_employee_id():
    
    return get_next_employee_id()


def create_employee(name, department, skills):
    emp_id = generate_employee_id()
    employee = {
        "employee_id": emp_id,
        "name": name,
        "department": department,
        "skills": skills,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    logger.info(f"Employee Created: {employee}")
    return employee

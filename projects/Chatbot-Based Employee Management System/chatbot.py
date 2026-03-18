from llm_parser import parse_user_input
from employee_service import create_employee
from database_mongo import save_employee


def chatbot_response(message):
    data = parse_user_input(message)
    employee = create_employee(data["name"], data["department"], data["skills"])
    save_employee(employee)
    return employee

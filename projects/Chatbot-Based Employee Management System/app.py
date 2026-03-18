from flask import Flask, render_template, request, jsonify
from chatbot import chatbot_response
from config import API_KEY
from database_mongo import (
    save_employee,
    list_employees,
    find_employee_by_id,
    update_employee,
    delete_employee,
    count_employees,
)
from employee_service import create_employee

app = Flask(__name__)


def _require_api_key():
    if not API_KEY:
        return None
    provided = request.headers.get("X-API-Key")
    if provided != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return None


def _validate_employee_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return None, "Invalid JSON payload."

    fields = {}

    def _get_str(key):
        value = payload.get(key)
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            return "invalid"
        return value.strip()

    name = _get_str("name")
    department = _get_str("department")
    skills = payload.get("skills")

    if name == "invalid":
        return None, "Name must be a non-empty string."
    if department == "invalid":
        return None, "Department must be a non-empty string."

    if skills is not None:
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        if not isinstance(skills, list) or not all(
            isinstance(s, str) and s.strip() for s in skills
        ):
            return None, "Skills must be a list of non-empty strings."

    if not partial:
        if name is None or department is None or skills is None:
            return None, "name, department, and skills are required."

    if name is not None:
        fields["name"] = name
    if department is not None:
        fields["department"] = department
    if skills is not None:
        fields["skills"] = [s.strip() for s in skills if s.strip()]

    return fields, None


def _build_filters():
    filters = {}
    name = request.args.get("name")
    department = request.args.get("department")
    skill = request.args.get("skill")
    if name:
        filters["name"] = {"$regex": name, "$options": "i"}
    if department:
        filters["department"] = {"$regex": department, "$options": "i"}
    if skill:
        filters["skills"] = {"$elemMatch": {"$regex": skill, "$options": "i"}}
    return filters


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    auth = _require_api_key()
    if auth:
        return auth

    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    if not message:
        return jsonify({"error": "message is required."}), 400

    try:
        response = chatbot_response(message)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(response)


@app.route("/employees", methods=["POST"])
def create_employee_api():
    auth = _require_api_key()
    if auth:
        return auth

    payload = request.get_json(silent=True) or {}
    fields, error = _validate_employee_payload(payload, partial=False)
    if error:
        return jsonify({"error": error}), 400

    employee = create_employee(fields["name"], fields["department"], fields["skills"])
    save_employee(employee)
    return jsonify(employee), 201


@app.route("/employees", methods=["GET"])
def get_all_employees():
    filters = _build_filters()
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return jsonify({"error": "page and limit must be integers."}), 400
    if page < 1 or limit < 1 or limit > 100:
        return jsonify({"error": "page must be >=1 and limit between 1 and 100."}), 400

    skip = (page - 1) * limit
    employees = list_employees(filters, skip, limit)
    total = count_employees(filters)

    return jsonify({"employees": employees, "page": page, "limit": limit, "total": total})


@app.route("/employees/<employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = find_employee_by_id(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found."}), 404
    return jsonify(employee)


@app.route("/employees/<employee_id>", methods=["PUT"])
def update_employee_api(employee_id):
    auth = _require_api_key()
    if auth:
        return auth

    payload = request.get_json(silent=True) or {}
    fields, error = _validate_employee_payload(payload, partial=True)
    if error:
        return jsonify({"error": error}), 400
    if not fields:
        return jsonify({"error": "No fields to update."}), 400

    updated = update_employee(employee_id, fields)
    if not updated:
        return jsonify({"error": "Employee not found."}), 404
    return jsonify(updated)


@app.route("/employees/<employee_id>", methods=["DELETE"])
def delete_employee_api(employee_id):
    auth = _require_api_key()
    if auth:
        return auth

    deleted = delete_employee(employee_id)
    if not deleted:
        return jsonify({"error": "Employee not found."}), 404
    return jsonify({"deleted": True})


if __name__ == "__main__":
    app.run(debug=True)

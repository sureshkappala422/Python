def _split_skills(raw):
    for sep in [";", "|", "/"]:
        if sep in raw:
            return [s.strip() for s in raw.split(sep) if s.strip()]
    return [raw.strip()] if raw.strip() else []


def parse_user_input(message):
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")

    parts = [p.strip() for p in message.split(",") if p.strip()]
    if len(parts) < 3:
        raise ValueError("Expected format: Name, Department, Skill1/Skill2")

    name = parts[0]
    department = parts[1]
    skills = _split_skills(parts[2])

    return {"name": name, "department": department, "skills": skills}

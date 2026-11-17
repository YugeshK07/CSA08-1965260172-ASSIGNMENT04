import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def parse_registration(raw_line):
    """Expected: register,name,department,email,event1;event2"""
    fields = [field.strip() for field in raw_line.split(",", 4)]
    if len(fields) != 5:
        raise ValueError(f"expected 5 comma-separated fields, found {len(fields)}")
    register, name, department, email, events_text = fields
    if not register or not name or not department:
        raise ValueError("register number, name and department are required")
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError(f"invalid email address {email!r}")
    events = [event.strip() for event in events_text.split(";") if event.strip()]
    if not events:
        raise ValueError("at least one event is required")
    return {
        "register": register,
        "name": name,
        "department": department,
        "email": email,
        "events": events
    }

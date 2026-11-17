def calculate_stats(records):
    result = {}
    for register, days in records.items():
        present = sum(status == "P" for status in days.values())
        total = len(days)
        result[register] = {
            "present": present,
            "absent": total - present,
            "percentage": (present / total * 100) if total else 0.0,
            "three_consecutive_absences": has_three_consecutive_absences(days)
        }
    return result


def has_three_consecutive_absences(days):
    dates = sorted(days)
    for index in range(len(dates) - 2):
        first, second, third = dates[index:index + 3]
        if days[first] == days[second] == days[third] == "A":
            from datetime import date
            d1, d2, d3 = date.fromisoformat(first), date.fromisoformat(second), date.fromisoformat(third)
            if (d2 - d1).days == 1 and (d3 - d2).days == 1:
                return True
    return False

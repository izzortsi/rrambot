from typing import Dict

seconds_per_unit: Dict[str, int] = {
    "m": 60,
    "h": 60 * 60,
    "d": 24 * 60 * 60,
    "w": 7 * 24 * 60 * 60,
}

unit_to_relative_date: Dict[str, int] = {
    "m": lambda n: f"{n} min ago",
    "h": lambda n: f"{n} hours ago",
    "d": 24 * 60 * 60,
    "w": 7 * 24 * 60 * 60,
}

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Website:
    domain: str
    technologies: List[Dict]
    meta: Dict
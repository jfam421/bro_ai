from skills.programs import handle_programs
from skills.browser import handle_browser
from core.skill import Skill

SKILLS = [
    Skill("programs", handle_programs),
    Skill("browser", handle_browser),
]
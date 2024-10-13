from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "#6c99bb",
        "warning": "bold yellow",
        "error": "bold red",
        "success": "bold green",
        "help": "bold yellow",
        "board": "#e5b567",
        "prevboard": "#545252",
    }
)

console = Console(theme=custom_theme)



class color:

    def __init__(self, color: int):
        pass

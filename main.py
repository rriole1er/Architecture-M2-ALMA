from interface import CLI
from services.mininet_manager import MiniNetManager

if __name__ == "__main__":
    system = MiniNetManager()
    cli = CLI(system)
    cli.menu()
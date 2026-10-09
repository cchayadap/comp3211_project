"""View: console input/output loop."""
from controller import CommandController


def run_cli(controller: CommandController = None) -> None:
    controller = controller or CommandController()
    print("PIM system. Type 'help' for commands.")
    while controller.running:
        try:
            line = input("pim> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        output = controller.execute(line)
        if output:
            print(output)

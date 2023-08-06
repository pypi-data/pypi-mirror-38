from dlhub_cli.parsing import main_func
from dlhub_cli.commands import (
    init_cmd)


@main_func
def cli_root():
    pass


cli_root.add_command(init_cmd)
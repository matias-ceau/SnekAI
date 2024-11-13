"""SnekAI - CLI wrapper for jupyter, openai, ollama and other tools."""

import argparse
import os
import shlex
import sys
from os.path import dirname
from subprocess import run

SNEKAI_ROOT = dirname(dirname(dirname(__file__)))
SNEKAI_CONFIG = os.path.join(SNEKAI_ROOT, "config")

environment = dict(
    JUPYTER_CONFIG_DIR=os.path.join(SNEKAI_CONFIG, "etc", "jupyter"),
    JUPYTER_DATA_DIR=os.path.join(SNEKAI_CONFIG, "share", "jupyter"),
    # JUPYTER_RUNTIME_DIR=os.path.join(SNEKAI_CONFIG, "jupyter_runtime"),
    IPYTHON_DIR=os.path.join(SNEKAI_CONFIG, "ipython"),
)

# if 'snekai' not in os.environ.get("VIRTUAL_ENV", "it's actualy written snake!"):

cmd_prefix = [f"{k}={v}" for k, v in environment.items()]


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Snekai - CLI wrapper for jupyter, openai, ollama and other tools."
    )
    parser.add_argument(
        "cmd",
        choices=["ipython", "notebook", "lab", "jupyter", "help"],
        help="Command to run (notebook, lab, jupyter)",
    )
    parser.add_argument(
        "opts",
        nargs=argparse.REMAINDER,
        help="Arguments for the command. Run 'snek help <command>' for help.",
    )

    args = parser.parse_args()

    match args.cmd:
        case "ipython":
            cmd = ["ipython"] + args.opts
        case "notebook":
            cmd = ["jupyter-notebook"] + args.opts
        case "lab":
            cmd = ["jupyter-lab"] + args.opts
        case "jupyter":
            cmd = ["jupyter"] + args.opts
        case "help":
            if args.opts:
                match args.opts[0]:
                    case "ipython":
                        cmd = ["ipython", "--help"]
                    case "notebook":
                        cmd = ["jupyter-notebook", "--help"]
                    case "lab":
                        cmd = ["jupyter-lab", "--help"]
                    case "jupyter":
                        cmd = ["jupyter", "--help"]
                    case _:
                        print("Unknown command")
                        sys.exit(1)
            else:
                print("Usage: snek help <command>")
                sys.exit(1)
    if cmd:
        run(shlex.join(cmd_prefix + cmd), shell=True)


if __name__ == "__main__":
    main()

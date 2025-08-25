import subprocess
import sys


def run_celery() -> None:
    """Run celery as a subprocess."""
    command = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "appsconfig",
        "worker",
        "-l",
        "info",
    ]
    subprocess.run(command, check=True)  # noqa: S603


if __name__ == "__main__":
    run_celery()

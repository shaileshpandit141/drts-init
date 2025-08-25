import subprocess
import sys


def run_celery() -> None:
    """Run Celery as a subprocess."""
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

    try:
        subprocess.run(command, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Celery failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Celery is not installed in the current environment.")
        sys.exit(1)


if __name__ == "__main__":
    run_celery()

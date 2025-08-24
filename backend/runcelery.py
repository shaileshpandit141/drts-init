from appsconfig.celery import app


def run_celery(
    queues: list[str] | None = None,
    loglevel: str = "info",
    concurrency: int = 1,
) -> None:
    """Run a Celery worker for Django programmatically."""
    argv = [
        "worker",
        f"--loglevel={loglevel}",
        f"--concurrency={concurrency}",
    ]

    if queues:
        argv.append(f"--queues={','.join(queues)}")

    app.worker_main(argv)  # type: ignore  # noqa: PGH003


if __name__ == "__main__":
    run_celery(
        queues=["default", "emails", "priority"],
        loglevel="info",
        concurrency=4,
    )

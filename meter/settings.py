import os


class Settings:
    SLEEP_TIMEOUT_SECONDS = int(os.environ.get("SLEEP_TIMEOUT_SECONDS", 60))

    # rabbit
    RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
    RABBIT_PORT = int(os.environ.get("RABBIT_PORT", 5672))
    RABBIT_LOGIN = os.environ.get("RABBIT_LOGIN", "guest")
    RABBIT_PASSWORD = os.environ.get("RABBIT_PASSWORD", "guest")


settings = Settings

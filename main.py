from views.main_view import main
from config.settings import SENTRY_DSN
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
    )

if __name__ == "__main__":
    main()

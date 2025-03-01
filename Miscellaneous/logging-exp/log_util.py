import os
from job_context import logger as context_logger
from dotenv import load_dotenv

load_dotenv()

ENABLE_LOGGING = False if os.getenv("ENABLE_LOGGING",
                                    "true").lower() == "false" else True

def log_message(message: str, logger=None):
    """Log the message

    Parameters
    ----------
    message : str
        The message to be logged
    logger : _type_, optional
        The logger object, by default None

    Returns
    -------
    None
    """
    if logger is not None:
        logger.info(message)
    else:
        print(message)

logger = context_logger.get() if ENABLE_LOGGING else None
log_message(f"print statement:{28}", logger)


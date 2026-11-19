
import logging
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord):
        output = {
        "timestamp": datetime.fromtimestamp(record.created).isoformat(),
        "level": record.levelname,
        "message": record.getMessage(),
        "event": getattr(record, "event", "general"),
        "reason": getattr(record, "reason", None)
        }
        return json.dumps(output)
    
def get_logger():
    logger = logging.getLogger("geospatial")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    return logger
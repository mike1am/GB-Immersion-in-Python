import time
import logging
from functools import wraps

LOG_FORMAT = "{levelname}: {asctime}  Logger: {name}  Method: {funcName}{args}  {msg}"
logging.basicConfig(
    format=LOG_FORMAT,
    style="{",
    filename="HW15.log",
    encoding="utf-8",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

perfLogger = logging.getLogger("PerfLog")
perfLogger.setLevel(logging.INFO)
fileHandler = logging.FileHandler("perf.log", encoding="utf-8")
formatter = logging.Formatter("{asctime}  Method: {funcName}{args}  {msg}", style="{")
fileHandler.setFormatter(formatter)
perfLogger.addHandler(fileHandler)
perfLogger.propagate = False


def perfLog(logger=perfLogger):
    def inner(func):
        @wraps(func)
        def perfLogWrapper(*args, **kwargs):
            start = time.perf_counter()
            
            res = func(*args, **kwargs)
            
            logger.info(f"Function: {func.__name__:<20}  Exec. time: {time.perf_counter() - start:.5f}")
            return res
    
        return perfLogWrapper
    return inner

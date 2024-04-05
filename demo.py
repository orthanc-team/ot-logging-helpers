from ot_logging_helpers import LogContext, configure_logging
import logging
import threading

configure_logging()

logger = logging.getLogger("DEMO")

with LogContext("1ST"):
    logger.info("my first message")
    with LogContext("2ND"):
        logger.info("my second message")


def worker(worker_id):
    with LogContext(f"Worker {worker_id}"):
        logger.info("my top level worker message")

        with LogContext("next-context"):
            logger.warning("my warning")

for i in range(0, 2):
    thread = threading.Thread(target=worker, args=(i+1, ))
    thread.start()


###### this shall output 
# 2024-04-05 16:41:09,429 - DEMO - INFO     -  1ST | my first message
# 2024-04-05 16:41:09,430 - DEMO - INFO     -  1ST | 2ND | my second message
# 2024-04-05 16:41:09,433 - DEMO - INFO     -  Worker 1 | my top level worker message
# 2024-04-05 16:41:09,433 - DEMO - WARNING  -  Worker 1 | next-context | my warning
# 2024-04-05 16:41:09,435 - DEMO - INFO     -  Worker 2 | my top level worker message
# 2024-04-05 16:41:09,436 - DEMO - WARNING  -  Worker 2 | next-context | my warning

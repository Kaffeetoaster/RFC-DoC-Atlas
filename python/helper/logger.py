import logging
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict


@dataclass
class TimingStat:
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0

    def add(self, value_ms: float) -> None:
        self.count += 1
        self.total_ms += value_ms
        self.min_ms = min(self.min_ms, value_ms)
        self.max_ms = max(self.max_ms, value_ms)

    @property
    def avg_ms(self) -> float:
        if self.count == 0:
            return 0.0
        return self.total_ms / self.count


TIMING_STATS: Dict[str, TimingStat] = defaultdict(TimingStat)


def setup_logger(log_path: str = "time.log", logger_name: str = "atlas") -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers when called multiple times.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


@contextmanager
def timed(logger: logging.Logger, label: str, **context):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        TIMING_STATS[label].add(elapsed_ms)

        if context:
            context_str = " ".join(f"{key}={value}" for key, value in context.items())
            logger.info("timed label=%s ms=%.3f %s", label, elapsed_ms, context_str)
        else:
            logger.info("timed label=%s ms=%.3f", label, elapsed_ms)


def log_timing_summary(logger: logging.Logger) -> None:
    logger.info("---- timing summary ----")
    for label, stat in sorted(TIMING_STATS.items()):
        logger.info(
            "label=%s count=%d total_ms=%.3f avg_ms=%.3f min_ms=%.3f max_ms=%.3f",
            label,
            stat.count,
            stat.total_ms,
            stat.avg_ms,
            stat.min_ms,
            stat.max_ms,
        )


# Example usage in main.py (commented out on purpose):
#
# from python.helper.logger import setup_logger, timed, log_timing_summary
#
# logger = setup_logger("time.log")
#
# with timed(logger, "main.total"):
#     with timed(logger, "draw_religion_maps.total"):
#         for iReligion in range(iNumReligions):
#             with timed(logger, "draw_religion_map.single", religion=iReligion):
#                 draw_religion_map(iReligion, layers_config)
#
# # Summary example (call once near the end of the run):
# # log_timing_summary(logger)

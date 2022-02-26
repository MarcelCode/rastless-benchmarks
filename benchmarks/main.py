import os.path
from typing import List
import gevent
from locust.env import Environment
from locust import stats
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter, PERCENTILES_TO_REPORT
from locust.log import setup_logging
from datetime import datetime

from benchmarks.rastless_locust import RastLessVisualization

setup_logging("INFO", None)
stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5


def start_locust_runner(user_classes: List, user_count: int, spawn_rate: float, stop_after_seconds: int, csv_path: str,
                        csv_timestamp: bool = False):
    env = Environment(user_classes=user_classes)
    env.create_local_runner()
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    if csv_timestamp:
        csv_path = f"{csv_path}_{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"

    csv_stats = StatsCSVFileWriter(env, PERCENTILES_TO_REPORT, csv_path)
    gevent.spawn(csv_stats.stats_writer)

    env.runner.start(user_count, spawn_rate=spawn_rate)

    gevent.spawn_later(stop_after_seconds, lambda: env.runner.quit())
    env.runner.greenlet.join()


if __name__ == '__main__':
    start_locust_runner([RastLessVisualization], user_count=10, spawn_rate=1, stop_after_seconds=11,
                        csv_path="../benchmark_results/rastless/visualization")

import os
from typing import List
import gevent
from locust.env import Environment
from locust import stats
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter, PERCENTILES_TO_REPORT
from locust.log import setup_logging
from datetime import datetime
from benchmarks.settings import Settings

from benchmarks import rastless_locust
from benchmarks import rasdaman_locust

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
    USER_COUNT = 25
    SPAWN_RATE = 1
    STOP_AFTER_SECONDS = 35

    # start_locust_runner([rastless_locust.RastLessVisualization], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rastless/visualization"))
    #
    # start_locust_runner([rasdaman_locust.RasdamanProxyVisualization], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman/visualization"))
    #
    # start_locust_runner([rasdaman_locust.RasdamanLocalVisualization], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman_local/visualization"))
    #
    # start_locust_runner([rasdaman_locust.RasdamanProxyPointAnalysis], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman/analysis_point"))

    # start_locust_runner([rasdaman_locust.RasdamanProxyPointAnalysis], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman/analysis_polygon"))

    # start_locust_runner([rasdaman_locust.RasdamanLocalPointAnalysis], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
    #                     stop_after_seconds=STOP_AFTER_SECONDS,
    #                     csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman_local/analysis_point"))

    start_locust_runner([rasdaman_locust.RasdamanLocalPolygonAnalysis], user_count=USER_COUNT, spawn_rate=SPAWN_RATE,
                        stop_after_seconds=STOP_AFTER_SECONDS,
                        csv_path=os.path.join(Settings.base_dir, "benchmark_results/rasdaman_local/analysis_polygon"))

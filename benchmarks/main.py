import os.path
import subprocess
from typing import List
import locust.stats

from benchmarks.utils.tools import get_stat_path
from benchmarks.settings import Settings

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 5
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.99]


TEST_TYPE_SETTINGS = {
    "visualization": {
        "rasdaman-local": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanLocalVisualization"
        },
        "rasdaman-proxy": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanProxyVisualization"
        },
        "rastless": {
            "file": "benchmarks/rastless_locust.py",
            "class": "RastLessVisualization"
        }
    },
    "point-analysis": {
        "rasdaman-local": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanLocalPointAnalysis"
        },
        "rasdaman-proxy": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanProxyPointAnalysis"
        },
        "rastless": {
            "file": "benchmarks/rastless_locust.py",
            "class": "RastLessPointAnalysis"
        }
    },
    "polygon-analysis": {
        "rasdaman-local": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanLocalPolygonAnalysis"
        },
        "rasdaman-proxy": {
            "file": "benchmarks/rasdaman_locust.py",
            "class": "RasdamanProxyPolygonAnalysis"
        },
        "rastless": {
            "file": "benchmarks/rastless_locust.py",
            "class": "RastLessPolygonAnalysis"
        }
    }
}


def run_test(test_type, systems: List[str], user_count: int, spawn_rate: float, run_time: str, add_timestamp=False):
    test_type_settings = TEST_TYPE_SETTINGS[test_type]

    for system in systems:
        system_settings = test_type_settings[system]

        stat_directory = get_stat_path(system, test_type, user_count, spawn_rate, run_time, add_timestamp)

        command = ["locust", "-f", os.path.join(Settings.base_dir, system_settings['file']),
                   system_settings['class'], "--headless", "--users", str(user_count),
                   "--spawn-rate", str(spawn_rate), "--run-time", run_time,
                   "--csv", stat_directory]

        subprocess.call(command)


if __name__ == '__main__':
    USER_COUNT = 20
    SPAWN_RATE = 1
    RUN_TIME = "21s"

    run_test("polygon-analysis", ["rastless"], USER_COUNT, SPAWN_RATE, RUN_TIME)

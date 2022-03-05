import os.path
import subprocess
import time
from typing import List
from datetime import datetime

from utils.tools import get_stat_path
from settings import Settings

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


def run_test(environment: str, test_type: str, systems: List[str], user_count: int, spawn_rate: float, run_time: str,
             add_timestamp=False):
    test_type_settings = TEST_TYPE_SETTINGS[test_type]

    timestamp = None
    if add_timestamp:
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    for system in systems:
        system_settings = test_type_settings[system]
        print(system_settings)
        stat_directory = get_stat_path(Settings.base_dir, environment, system, test_type, user_count, spawn_rate,
                                       run_time, Settings.entries, timestamp)

        command = ["locust", "-f", os.path.join(Settings.base_dir, system_settings['file']),
                   system_settings['class'], "--headless", "--users", str(user_count),
                   "--spawn-rate", str(spawn_rate), "--run-time", run_time,
                   "--csv", stat_directory]

        subprocess.call(command)
        # print(" ".join(command))
        time.sleep(2)


if __name__ == '__main__':
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    run_test(ENVIRONMENT, "visualization", ["rasdaman-local", "rastless", "rasdaman-proxy"], 25, 1, "41s",
             add_timestamp=True)

    run_test(ENVIRONMENT, "point-analysis", ["rasdaman-local", "rastless", "rasdaman-proxy"], 10, 1, "31s",
             add_timestamp=True)

    run_test(ENVIRONMENT, "polygon-analysis", ["rasdaman-local", "rastless", "rasdaman-proxy"], 10, 1, "31s",
             add_timestamp=True)

import os
from main import run_test

if __name__ == '__main__':
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    user_count = 20
    spawn_rate = 20
    runtime = "61s"

    run_test(ENVIRONMENT, "visualization", ["rasdaman-local", "rasdaman-proxy"], user_count, spawn_rate,
             runtime, add_timestamp=True)

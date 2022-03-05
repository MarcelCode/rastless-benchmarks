import os
from main import run_test

if __name__ == '__main__':
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    run_test(ENVIRONMENT, "polygon-analysis", ["rasdaman-local", "rastless", "rasdaman-proxy"], 25, 1, "41s",
             add_timestamp=True)
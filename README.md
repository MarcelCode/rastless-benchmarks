# Start Headless

locust -f benchmarks/rastless_locust.py RastLessVisualization -u 10 -r 1 --csv=benchmark_results/rastless/visualization --headless -t11s
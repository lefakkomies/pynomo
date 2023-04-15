def pytest_runtest_logreport(report):
    if report.when == "call":
        test_name = report.nodeid.split("::")[-1]
        outcome = report.outcome.upper()
        color_str = "\x1b[31m"
        if outcome == "PASSED":
            color_str = '\x1b[32m'
        print(f"\nTest function: {test_name} -> {color_str}{outcome}\x1b[0m")

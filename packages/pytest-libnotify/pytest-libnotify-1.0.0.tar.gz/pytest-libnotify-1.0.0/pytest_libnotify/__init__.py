import pytest
import random
import subprocess


ID = "3495824895"
RED = "#B70404"
GREEN = "#0BA603"
NAME = ""


failed, passed, overall = 0, 0, 0
failures = []


@pytest.hookimpl()
def pytest_collection_finish(session):
    global NAME, overall
    NAME = session.name
    overall = len(session.items)


@pytest.hookimpl()
def pytest_runtest_logreport(report):
    global failed, passed, overall, failures
    if report.when == 'call':
        if report.outcome == 'passed':
            passed += 1
        else:
            failed += 1
            if len(failures) < 10:
                failures.append(report.nodeid.split("[")[0])
        if failed > 0:
            show_report(
                msg="{} of {} tests run, {} failed\n{}".format(
                    failed + passed, overall, failed, "\n".join(failures)
                ),
                color=RED,
            )
        else:
            show_report(
                msg="{} of {} tests passed".format(passed, overall), color=GREEN
            )


@pytest.hookimpl()
def pytest_terminal_summary(terminalreporter, exitstatus):
    stats = terminalreporter.stats
    failures = stats.get('failed', [])
    failed = len(failures)
    passed = len(stats.get('passed', []))
    show_failures = "\n".join([report.nodeid.split("[")[0] for report in failures[:10]])
    if exitstatus > 0:
        show_report(
            msg="{} of {} tests failed\n{}".format(
                failed, failed + passed, show_failures
            ),
            color=RED,
        )
    else:
        show_report(msg="{} tests passed".format(passed), color=GREEN)


def show_report(msg, color):
    subprocess.Popen(
        [
            "notify-send",
            "-r",
            ID,
            "-h",
            "string:bgcolor:{}".format(color),
            "{}: {}".format(NAME, msg),
        ]
    )

# Copyright © 2026 - Homewood Health Inc.

# Pytest configuration and shared fixtures
import csv
import os
from datetime import datetime

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from suites.CustomerPortal import CustomerPortal
from suites.Homeweb import Homeweb
from suites.QuantumAPI import QuantumAPI
from suites.SentioClient import SentioClient
from suites.SentioProvider import SentioProvider

# --- Report Collection ---

_env_results = {}
_versions = {}  # {"PROD": {"Homeweb": "v3.0.17.261", ...}, "BETA": {...}}


def _pct(r):
    total = r["passed"] + r["failed"]
    return f"{int(r['passed'] / total * 100)}%" if total > 0 else "N/A"


@pytest.fixture(scope="session")
def record_version():
    import re
    import requests

    def _record(label, base_url, env):
        try:
            r = requests.get(f"{base_url}/version.html", timeout=5, verify=False)
            match = re.search(r"v?\d+\.\d+\.\d+\.\d+", r.text)
            raw = match.group(0) if match else "N/A"
            version = raw if raw == "N/A" or raw.startswith("v") else f"v{raw}"
        except Exception:
            version = "N/A"
        env_key = env.upper()
        if env_key not in _versions:
            _versions[env_key] = {}
        _versions[env_key][label] = version

    return _record


def pytest_runtest_logreport(report):
    if report.when == "setup" and report.skipped:
        phase = "skipped"
    elif report.when == "call":
        if report.passed:
            phase = "passed"
        elif report.failed:
            phase = "failed"
        elif report.skipped:
            phase = "skipped"
        else:
            return
    else:
        return

    name = report.nodeid
    if "[PROD]" in name:
        env = "PROD"
    elif "[BETA]" in name:
        env = "BETA"
    else:
        env = "PROD"

    if env not in _env_results:
        _env_results[env] = {"passed": 0, "failed": 0, "skipped": 0}

    _env_results[env][phase] += 1


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not _env_results:
        return

    envs = ["PROD", "BETA"]
    results = {e: _env_results.get(e, {"passed": 0, "failed": 0, "skipped": 0}) for e in envs}

    total_passed = sum(r["passed"] for r in results.values())
    total_failed = sum(r["failed"] for r in results.values())
    total_skipped = sum(r["skipped"] for r in results.values())
    total_completed = total_passed
    total_run = total_passed + total_failed
    total_pct = f"{int(total_passed / total_run * 100)}%" if total_run > 0 else "N/A"

    # Build version strings per env: "Label: version\nLabel: version\n..."
    prod_versions_str = "\n".join(
        f"{label}: {ver}" for label, ver in _versions.get("PROD", {}).items()
    )
    beta_versions_str = "\n".join(
        f"{label}: {ver}" for label, ver in _versions.get("BETA", {}).items()
    )

    sep = "-" * 52
    terminalreporter.write_sep("=", "TEST REPORT")

    if _versions:
        prod_lines = prod_versions_str.splitlines()
        beta_lines = beta_versions_str.splitlines()
        for i in range(max(len(prod_lines), len(beta_lines))):
            p = prod_lines[i] if i < len(prod_lines) else ""
            b = beta_lines[i] if i < len(beta_lines) else ""
            terminalreporter.write_line(f"  {p:<33} {b}")
        terminalreporter.write_line("")

    terminalreporter.write_line(f"{'Metric':<35} {'PROD':>7} {'BETA':>7}")
    terminalreporter.write_line(sep)
    terminalreporter.write_line(f"{'Passed':<35} {results['PROD']['passed']:>7} {results['BETA']['passed']:>7}")
    terminalreporter.write_line(f"{'Failed':<35} {results['PROD']['failed']:>7} {results['BETA']['failed']:>7}")
    terminalreporter.write_line(f"{'Not Run (Skipped, N/A, etc.)':<35} {results['PROD']['skipped']:>7} {results['BETA']['skipped']:>7}")
    terminalreporter.write_line(f"{'Completed':<35} {results['PROD']['passed'] + results['PROD']['failed']:>7} {results['BETA']['passed'] + results['BETA']['failed']:>7}")
    terminalreporter.write_line(f"{'Percentage Passed':<35} {_pct(results['PROD']):>7} {_pct(results['BETA']):>7}")
    terminalreporter.write_line(sep)
    terminalreporter.write_line(f"{'Total Passed':<35} {total_passed:>7}")
    terminalreporter.write_line(f"{'Total Failed':<35} {total_failed:>7}")
    terminalreporter.write_line(f"{'Total Not Run':<35} {total_skipped:>7}")
    terminalreporter.write_line(f"{'Total Completed':<35} {total_completed:>7}")
    terminalreporter.write_line(f"{'Total Percentage Passed':<35} {total_pct:>7}")

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_map = {
        "test_bat_web": "bat",
        "test_bat_homeweb": "bat_homeweb",
        "test_bat_customer_portal": "bat_customer_portal",
        "test_bat_sentio_client": "bat_sentio_client",
        "test_bat_sentio_provider": "bat_sentio_provider",
    }
    file_args = [a for a in config.invocation_params.args if a.endswith(".py")]
    if file_args:
        stem = os.path.basename(file_args[0]).replace(".py", "")
        report_name = name_map.get(stem, stem.replace("test_", ""))
    else:
        report_name = "bat"
    csv_path = f"reports/{report_name}_{timestamp}.csv"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "PROD", "BETA", "Total"])
        writer.writerow(["Versions", prod_versions_str, beta_versions_str, ""])
        writer.writerow(["Passed", results["PROD"]["passed"], results["BETA"]["passed"], total_passed])
        writer.writerow(["Failed", results["PROD"]["failed"], results["BETA"]["failed"], total_failed])
        writer.writerow(["Not Run (Skipped, N/A, etc.)", results["PROD"]["skipped"], results["BETA"]["skipped"], total_skipped])
        writer.writerow(["Completed", results["PROD"]["passed"], results["BETA"]["passed"], total_completed])
        writer.writerow(["Percentage Passed", _pct(results["PROD"]), _pct(results["BETA"]), total_pct])

    terminalreporter.write_line(f"\n  Report saved: {csv_path}")


@pytest.fixture(scope="session")
def driver(env):
    # 1: Configure Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 2: Launch Browser
    driver_instance = webdriver.Chrome(options=chrome_options)

    # 3. YIELD - give driver to the tests
    yield driver_instance

    # 4: Close Browser
    driver_instance.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment: prod | beta | all"
    )
    # parser.addoption(
    #     "--lang",
    #     action="store",
    #     default="en",
    #     help="Language: en | fr | all"
    # )


def pytest_collection_modifyitems(items):
    def get_group(item):
        name = item.name

        import re
        match = re.search(r"test_bat_web_(\d+)", name)
        order = int(match.group(1)) if match else 999

        # 🔥 ENV FIRST (this is the fix)
        if "[PROD]" in name:
            env = 0
        elif "[BETA]" in name:
            env = 1
        elif "_beta" in name.lower():
            env = 1
        else:
            env = 2

        return env, order

    items.sort(key=get_group)


@pytest.fixture(params=["prod", "beta"], ids=["PROD", "BETA"], scope="session")
def env(request):
    env_flag = request.config.getoption("--env")

    if env_flag != "all" and request.param != env_flag:
        pytest.skip(f"Skipping {request.param} environment")

    return request.param


load_dotenv()


@pytest.fixture(scope="session")
def credentials():
    return {
        "personal": {
            "email": os.getenv("PERSONAL_EMAIL"),
            "password": os.getenv("PERSONAL_PASSWORD")
        },
        "dsg_demo": {
            "email": os.getenv("DSG_DEMO_EMAIL"),
            "password": os.getenv("DSG_DEMO_PASSWORD")
        },
        "sentio": {
            "email": os.getenv("SENTIO_EMAIL"),
            "password": os.getenv("SENTIO_PASSWORD")
        },
        "hhi_demo": {
            "email": os.getenv("HHI_DEMO_EMAIL"),
            "password": os.getenv("HHI_DEMO_PASSWORD")
        },
        "lso_test": {
            "email": os.getenv("LSO_EMAIL"),
            "password": os.getenv("LSO_PASSWORD")
        }
    }


@pytest.fixture(scope="session")
def language():
    return os.getenv("LANGUAGE", "en")


@pytest.fixture(scope="session")
def quantum(driver, language, env):
    return QuantumAPI(driver, language, env)


@pytest.fixture(scope="session")
def homeweb(driver, language, env, quantum):
    return Homeweb(driver, language, env, quantum)


@pytest.fixture(scope="session")
def customer_portal(driver, language, env, quantum):
    if env == "beta":
        return pytest.skip(f"Skipping {env} environment")
    else:
        return CustomerPortal(driver, language, env, quantum)


@pytest.fixture(scope="session")
def quantum_prod(driver, language):
    return QuantumAPI(driver, language, "prod")


@pytest.fixture(scope="session")
def sentio_client(driver, language, env, quantum, quantum_prod):
    if env == "prod":
        return pytest.skip(f"Skipping {env} environment")
    else:
        # TODO: Switch back on MONDAY 03-30-2026
        return SentioClient(driver, language, env, quantum_prod)
        # return SentioClient(driver, language, env, quantum)


@pytest.fixture(scope="session")
def sentio_provider(driver, language, env, quantum, quantum_prod):
    if env == "prod":
        return pytest.skip(f"Skipping {env} environment")
    else:
        return SentioProvider(driver, language, env, quantum_prod)

"""Keeps CI green until the first real tests land: pytest exits with code 5 when it collects nothing."""


def test_ci_runs():
    assert True

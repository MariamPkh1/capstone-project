"""Every test runs offline: no key, no network, no cost. The tool log goes to a temp folder."""
import os
import tempfile

os.environ["ABITURIENTI_TOOL_LOG"] = os.path.join(tempfile.mkdtemp(prefix="abiturienti-tests-"), "tools.jsonl")

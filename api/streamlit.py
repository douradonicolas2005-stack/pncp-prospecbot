import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
from streamlit.web import bootstrap
def main():
    bootstrap.run(
        os.path.join(ROOT_DIR, "dashboard.py"),
        is_hello=False,
        args=[],
        flag_options={
            "server.port": os.environ.get("PORT", "8501"),
            "server.address": "0.0.0.0",
            "server.headless": True,
            "server.enableCORS": False,
            "server.enableXsrfProtection": False,
            "browser.gatherUsageStats": False,
        },
    )
if __name__ == "__main__":
    main()

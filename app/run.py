import streamlit.web.cli as stcli
from pathlib import Path
import sys

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        str(Path(__file__).parent / 'app' / "app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
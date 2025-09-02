# logic/commands/close_app.py

from kivy.app import App
import sys

def close_app():
    """Gracefully stop the Kivy app and exit."""
    app = App.get_running_app()
    if app:
        app.stop()
    sys.exit(0)

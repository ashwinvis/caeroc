import subprocess
import sys


def caeroc_app():
    import caeroc

    try:
        caeroc.launch()
    except AttributeError:
        app = caeroc.gui.CalcApp()
        app.run()


def caeroc_test():
    try:
        subprocess.call("caeroc-app", timeout=4)
    except subprocess.TimeoutExpired:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    caeroc_app()

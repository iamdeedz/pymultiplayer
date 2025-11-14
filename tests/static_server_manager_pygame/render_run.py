from multiprocessing import Process
from subprocess import run


def run_http():
    run(["python", "-m", "http.server", "8000"])


if __name__ == "__main__":
    Process(target=run_http).start()
    run(["python", "server.py"])
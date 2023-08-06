from setuptools import setup

if __name__ == "__main__":
    console_scripts = ["timeit = shell_timeit._timeit:entry"]
    setup(entry_points=dict(console_scripts=console_scripts))

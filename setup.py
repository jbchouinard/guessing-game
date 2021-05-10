from setuptools import setup, find_packages

try:
    from Cython.Build import cythonize

    ext_modules = cythonize("guessgame/fastcheck.pyx")
except ImportError:
    print("cython not found, will use slow check function")
    ext_modules = []

setup(
    name="guessgame",
    version="1.0.0",
    url="https://github.com/jbchouinard/guess-game.git",
    author="Jerome Boisvert-Chouinard",
    author_email="me@jbchouinard.net",
    description="Guessing game and solver.",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "guessgame = guessgame.gui:main",
            "guessgame-benchmark = guessgame.solver:main",
        ]
    },
    ext_modules=ext_modules,
)

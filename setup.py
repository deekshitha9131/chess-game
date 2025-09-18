from setuptools import setup, find_packages

setup(
    name="chess-game",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame>=2.0.0",
        "python-chess>=1.999"
    ],
    package_data={
        "chess_game": ["assets/*.png"]
    },
    entry_points={
        "console_scripts": [
            "chess-game=chess_game.main:main"
        ]
    }
)
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vizpa",
    version="1.0.0",
    author="Shrihari",
    author_email="shariethernet@gmail.com",
    description="A Framework to VIZualize Power and Area of a RTL Design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vizpa",
    packages=["vizpa"],
    entry_points={
        "console_scripts": [
            "vizpa = vizpa.vizpa:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "plotly",
        "numpy",
        "pandas",
        "argparse"
    ],
)
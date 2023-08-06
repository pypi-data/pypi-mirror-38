from setuptools import setup


setup(
    name="gb",
    version="0.1",
    description="A Python gopher server.",
    url="https://github.com/supakeen/gb",
    author="supakeen",
    author_email="cmdr@supakeen.com",
    packages=[],
    install_requires=["tornado", "click"],
    entry_points={"console_scripts": ["gb=gb.command:main"]},
    tests_require=["nose", "aiounittest"],
    extras_require={"dev": ["pre-commit", "flake8", "black", "nose"]},
    test_suite="nose.collector",
)

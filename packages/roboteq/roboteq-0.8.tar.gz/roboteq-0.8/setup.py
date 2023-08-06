from setuptools import setup, find_packages

setup(
    name="roboteq",
    version="0.8",
    url="https://github.com/daltonpearson/roboteq",
    license="MIT",
    author="Dalton Pearson",
    author_email="daltonpearson1997@gmail.com",
    description="Port of the roboteq API",
    packages=find_packages(exclude=["tests"]),
    long_description=open("README.md").read(),
    zip_safe=False,
)

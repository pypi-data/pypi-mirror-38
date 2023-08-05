from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nk_logger",
    version="1.1.0",
    description="A python logger that plays nice with datadog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NewKnowledge/nk-logger',
    packages=["nk_logger"],
    include_package_data=True,
    install_requires=["python-json-logger"],
    license="MIT",
)

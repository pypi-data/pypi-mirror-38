from setuptools import setup


setup(
    name="nk_logger",
    version="1.0.0",
    description="A python logger that plays nice with datadog",
    packages=["nk_logger"],
    include_package_data=True,
    install_requires=["python-json-logger"],
)

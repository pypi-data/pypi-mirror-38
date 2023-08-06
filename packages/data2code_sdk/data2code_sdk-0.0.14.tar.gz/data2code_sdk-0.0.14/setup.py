from setuptools import setup, find_packages
setup(
    name="data2code_sdk",
    version="0.0.14",
    packages=find_packages(),
    # include_package_data=True,
    install_requires=["rigger_plugin_framework"],
)
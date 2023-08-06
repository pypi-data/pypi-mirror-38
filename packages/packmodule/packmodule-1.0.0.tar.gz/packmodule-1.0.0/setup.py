import setuptools
import os.path

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="packmodule",
    version="1.0.0",
    url="https://github.com/schlarpc/packmodule",
    description="Python code packer for CloudFormation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["packmodule"],
)

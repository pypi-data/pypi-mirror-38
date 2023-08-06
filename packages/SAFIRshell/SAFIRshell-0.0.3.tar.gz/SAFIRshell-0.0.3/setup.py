import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SAFIRshell",
    version="0.0.3",
    author="Ruben Van Coile",
    author_email="ruben.vancoile@gmail.com",
    description="SAFIR shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rvcoile/SAFIRshell",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
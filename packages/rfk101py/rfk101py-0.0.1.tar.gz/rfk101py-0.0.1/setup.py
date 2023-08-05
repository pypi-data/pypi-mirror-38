import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rfk101py",
    version="0.0.1",
    author="Michael Dubno",
    author_email="michael@dubno.com",
    description="RFK101 Proximity card reader over Ethernet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dubnom/rfk101py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

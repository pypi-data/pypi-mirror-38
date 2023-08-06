import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mona_client",
    version="0.0.1",
    author="MonaLabs",
    author_email="itai@monalabs.io",
    description="Client code for python Mona instrumentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/itai4/mona-python-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json_storage_manager",
    version="0.1.11",
    author="Ahmed Hefnawi",
    author_email="me@ahmedhefnawi.com",
    description="JSON Storage Manager for JSON data stored in text-files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hefnawi/json-storage-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_advanced_search_list_prod",
    version="0.0.1",
    author="Saurabh",
    author_email="saurabhrane.m@gmail.com",
    description="Package to advance search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saurabhranem/python_library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
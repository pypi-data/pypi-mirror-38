import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QuerysetPaginator",
    version="0.0.1",
    author="GetMeLive",
    author_email="tech@getmelive.in",
    description="This package helps in paginating evaluated querysets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GetMeLive/queryset-paginator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

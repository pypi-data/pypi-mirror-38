import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feature_explorer",
    version="0.0.1",
    author="Alberto Garza",
    author_email="albertogarza22@gmail.com",
    description="Web application for creating commonly useful data visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/garzillo/feature_explorer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
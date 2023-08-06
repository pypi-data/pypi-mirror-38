import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'bokeh>=1.0.1',
    'Click>=7.0',
    'Flask>=1.0.2',
    'itsdangerous>=1.1.0',
    'Jinja2==2.10',
    'MarkupSafe>=1.1.0',
    'numpy>=1.15.4',
    'packaging>=18.0',
    'pandas>=0.23.4',
    'Pillow>=5.3.0',
    'pyparsing>=2.3.0',
    'python-dateutil>=2.7.5',
    'pytz>=2018.7',
    'PyYAML>=3.13',
    'six>=1.11.0',
    'tornado>=5.1.1',
    'Werkzeug>=0.14.1',
]

setuptools.setup(
    name="feature_explorer",
    version="0.0.2",
    author="Alberto Garza",
    author_email="albertogarza22@gmail.com",
    description="Web application for creating commonly useful data visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/garzillo/feature_explorer",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
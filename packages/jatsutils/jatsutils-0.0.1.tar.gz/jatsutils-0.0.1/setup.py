import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jatsutils",
    version="0.0.1",
    author="Carlos Cesar Caballero",
    author_email="ccesar@daxslab.com",
    description="Utility for obtain JATS XML data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cccaballero/jatsutils",
    packages=setuptools.find_packages(),
    install_requires=[
        'lxml',
        'xmltodict'
    ],
    extras_require={
        'dev': [
            'tox',
            'tox-travis',
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

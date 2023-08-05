import setuptools

try:
    with open("README.rst", "r") as fd:
        long_description = fd.read()
except IOError:
    long_description = None  # Install without README.rst


setuptools.setup(
    name="elastic2-doc-manager",
    version="0.4.0",
    maintainer="mongodb",
    description="Elastic2 plugin for mongo-connector",
    long_description=long_description,
    platforms=["any"],
    author="anna herlihy",
    author_email="mongodb-user@googlegroups.com",
    url="https://github.com/mongodb-labs/elastic2-doc-manager",
    install_requires=["mongo-connector>=2.5.0"],
    extras_require={
        "aws": ["boto3 >= 1.4.0", "requests-aws-sign >= 0.1.2"],
        "elastic2": ["elasticsearch>=2.0.0,<3.0.0"],
        "elastic5": ["elasticsearch>=5.0.0,<6.0.0"],
    },
    packages=["mongo_connector", "mongo_connector.doc_managers"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
    ],
    keywords=["mongo-connector", "mongodb", "elastic", "elasticsearch"],
)

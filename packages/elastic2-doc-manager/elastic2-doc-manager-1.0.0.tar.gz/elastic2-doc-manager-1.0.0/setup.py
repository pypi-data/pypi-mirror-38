import setuptools

setuptools.setup(
    name="elastic2-doc-manager",
    use_scm_version=True,
    maintainer="mongodb",
    description="Elastic2 plugin for mongo-connector",
    platforms=["any"],
    author="anna herlihy",
    author_email="mongodb-user@googlegroups.com",
    url="https://github.com/mongodb-labs/elastic2-doc-manager",
    install_requires=["mongo-connector>=2.5.0", "importlib_metadata"],
    python_requires=">=3.4",
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
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
    ],
    keywords=["mongo-connector", "mongodb", "elastic", "elasticsearch"],
    setup_requires=["setuptools_scm>=1.15"],
)

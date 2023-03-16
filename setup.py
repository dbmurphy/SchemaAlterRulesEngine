import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schema-change-risk-engine",
    author="David Murphy",
    author_email="david.b.murphy.tx@gmail.com",
    description="Common MySQL Schema Alter Issues Check Engine Package",
    keywords="mysql, schema, ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbmruphy/SchemaAlterRulesEngine",
    project_urls={
        "Documentation": "https://github.com/dbmurphy/SchemaAlterRulesEngine",
        "Bug Reports": "https://github.com/dbmurphy/SchemaAlterRulesEngine/issues",
        "Source Code": "https://github.com/dbmurphy/SchemaAlterRulesEngine",
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={"schema-change-risk-engine": "schema_change_risk_engine"},
    packages=setuptools.find_packages(where="schema_change_risk_engine"),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # install_requires=['Pillow'],
    extras_require={
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)

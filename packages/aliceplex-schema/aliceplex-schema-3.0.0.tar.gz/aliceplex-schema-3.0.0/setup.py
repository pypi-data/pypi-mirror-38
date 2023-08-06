from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="aliceplex-schema",
    version="3.0.0",
    author="Alice Plex",
    url="https://github.com/aliceplex/schema",
    description="Schema library for Plex",
    tests_require=["pytest"],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=["aliceplex.schema"],
    setup_requires=["pytest-runner"],
    install_requires=["marshmallow>=3.0.0b20,<4.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ]
)

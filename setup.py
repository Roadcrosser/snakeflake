import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snakeflake",
    version="0.1.5.3",
    author="Roadcrosser",
    author_email="roadcrosser0@gmail.com",
    description="Snakeflake is a discrete nonserial ID generator like Snowflake implemented in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Roadcrosser/snakeflake",
    packages=setuptools.find_packages(),
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "http://roadcrosser.xyz/snakeflake/",
        "Source": "https://github.com/Roadcrosser/snakeflake",
    },
    python_requires=">=3.6",
)

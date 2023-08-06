import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="b64_cli",
    version="0.0.1",
    entry_points={
        "console_scripts": ['b64 = b64.b64:main']
    },
    author="Landon Gravat",
    author_email="railinator4903@gmail.com",
    description="A command line application to parse Base64 values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RailRunner16/b64_cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

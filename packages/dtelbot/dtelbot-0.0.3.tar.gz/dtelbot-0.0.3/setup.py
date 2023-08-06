import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtelbot",
    version="0.0.3",
    author="dalor",
    author_email="dalor@i.ua",
    description="Simple Telegram bot lib with regex checking and async features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
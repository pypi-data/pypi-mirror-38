import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instiz",
    version="0.1.1",
    author="Jonathan Nicholas",
    author_email="Jonathan.Nicholas@protonmail.com",
    description="A Python3-only library for iChart K-Pop chart scores.",
    install_requires=[
        "requests>=2.20.0",
        "beautifulsoup4>=4.6.3",
        "attrs>=18.2.0",
        "lxml>=4.2.5",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chromadream/instiz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
    ],
)

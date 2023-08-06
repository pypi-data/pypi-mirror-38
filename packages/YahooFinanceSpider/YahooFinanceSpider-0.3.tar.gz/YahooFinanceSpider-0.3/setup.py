import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YahooFinanceSpider",
    version="0.3",
    author="S-W-K",
    author_email="s979612095@gmail.com",
    description="A crawler of YahooFinace's Stock",
    keywords='japanese yahoo stock finance investment',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/S-W-K/YahooFinaceSpider",
    packages=setuptools.find_packages(),
    install_requires=[
        "lxml",
        "requests",
        "fake-useragent",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

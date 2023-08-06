import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraping_browser",
    version="0.0.3",
    author="Fabian Pflug",
    author_email="pflug@chi.uni-hannover.de",
    description="Web-Scraping browser emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gibraltar.chi.uni-hannover.de/pflug/browser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

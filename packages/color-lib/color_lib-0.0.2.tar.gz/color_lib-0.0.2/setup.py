import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="color_lib",
    version="0.0.2",
    author="Landon Gravat",
    author_email="railinator4903@gmail.com",
    description="Highlight your terminal output like a pro!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RailRunner16/color_lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

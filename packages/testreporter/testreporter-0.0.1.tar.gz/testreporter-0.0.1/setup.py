import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testreporter",
    version="0.0.1",
    author="Christo Crampton",
    author_email="christo@appointmentguru.co",
    description="Get pretty output for your Django unit tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/libs/dj-testreporter",
    packages=['.'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

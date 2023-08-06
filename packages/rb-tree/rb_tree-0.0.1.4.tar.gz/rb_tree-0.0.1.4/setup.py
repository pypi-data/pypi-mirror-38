import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rb_tree",
    version="0.0.1.4",
    author="Rishabh Bhatnagar",
    author_email="bhatnagarrishabh4@gmail.com",
    description="Manage rbt easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RishabhBhatnagar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

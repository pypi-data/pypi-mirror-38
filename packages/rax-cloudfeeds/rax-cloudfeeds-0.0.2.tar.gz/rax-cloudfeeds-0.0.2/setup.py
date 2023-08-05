import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rax-cloudfeeds",
    version="0.0.2",
    author="Customer And Racker Experience Team",
    author_email="CARE-CORERackers@rackspace.com",
    description="Client for Cloud Feeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.rackspace.com/andrew-dorrycott/cloudfeeds_client.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)

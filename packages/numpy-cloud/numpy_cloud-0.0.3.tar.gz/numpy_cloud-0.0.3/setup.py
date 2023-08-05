import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numpy_cloud",
    version="0.0.3",
    author="Numpy In The Cloud",
    author_email="author@example.com",
    description="Numpy in the cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ortutay/numpy_cloud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

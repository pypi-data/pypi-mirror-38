import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cascadepy",
    version="0.0.1",
    author="Simon Lu",
    author_email="mlu18@dons.usfca.edu",
    description="An extremely light weight distributed volunteer computing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
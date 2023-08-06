import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

	
setuptools.setup(
    name="etl_pipeline",
    version="0.0.2",
    author="Rinesh P R",
    author_email="rineshpr90@gmail.com",
    description="package for performing etl processing on csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
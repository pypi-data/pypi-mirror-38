import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binhash",
    version="0.2",
    author="Karthik Revanuru , Raghav Kulkarni , Rameshwar Pratap",
    author_email="karthik.revanuru@outlook.com",
    description="Algorithm to compress sparse binary data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KarthikRevanuru/binhash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
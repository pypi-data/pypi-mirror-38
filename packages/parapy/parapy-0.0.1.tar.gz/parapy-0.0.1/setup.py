import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parapy",
    version="0.0.1",
    author="Roald Simonsen",
    author_email="roald.frej@hotmail.com",
    description="An automatic handling of parameter passing to python programs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/archStant/parapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)

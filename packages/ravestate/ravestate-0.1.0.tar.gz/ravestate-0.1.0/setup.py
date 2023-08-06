import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ravestate",
    version="0.1.0",
    author="Roboy",
    author_email="info@roboy.org",
    # description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roboy/ravestate",
    package_dir={'': 'modules'},
    packages=setuptools.find_packages("modules"),
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
)
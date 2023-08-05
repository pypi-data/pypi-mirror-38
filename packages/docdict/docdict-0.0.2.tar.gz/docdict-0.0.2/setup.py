import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []

tests_require = [
    "pytest",
]

setuptools.setup(
    name="docdict",
    version="0.0.2",
    author="Slavik Nychkalo",
    author_email="slavik.nychkalo@gmail.com",
    description="Generate dict by docstrings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gebeto/docdict",
    install_requires=install_requires,
    tests_require=tests_require,
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mor0.1",
    version="0.0.1",
    author="Vanneste Felix",
    author_email="felix.vanneste@inria.fr",
    description="This mor package is a simple GUI to help user perform model order reduction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SofaDefrost/ModelOrderReduction",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent"
    ],
    install_requires=['cheetah','PyQt4','yaml']
)

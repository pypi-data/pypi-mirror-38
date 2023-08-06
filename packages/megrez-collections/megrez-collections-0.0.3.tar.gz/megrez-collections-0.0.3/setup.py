import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="megrez-collections",
    keywords=("megrez", "collections"),
    version="0.0.3",
    author="megrez",
    author_email="megez@z6x.org",
    description="megrez util collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.17zuoye.net/megrez/megrez-collections",
    namespace_packages=["megrez", ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
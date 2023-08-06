import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygtt",
    version="1.1.2",
    author="Eliseo Martelli",
    author_email="me@eliseomartelli.it",
    description="A python package to get GTT transit info",
    long_description=long_description,
    url="https://github.com/eliseomartelli/pygtt",
    packages=setuptools.find_packages(),
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
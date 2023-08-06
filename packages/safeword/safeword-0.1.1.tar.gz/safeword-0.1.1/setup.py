import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="safeword",
    version="0.1.1",
    author="eht",
    author_email="jared@e.ht",
    description="A small utility for generating character slugs on demand.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/e-ht/safeword",
    packages=setuptools.find_packages(),
    package_data={'safeword': ['resources/wordlist.csv', 'resources/wordlist.json']},
    license="Unlicense",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: Public Domain",
    ],
)

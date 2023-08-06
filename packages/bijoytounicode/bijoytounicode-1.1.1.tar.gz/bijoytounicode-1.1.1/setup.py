import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bijoytounicode",
    version="1.1.1",
    author="Utsob Roy",
    author_email="roy@codesign.com.bd",
    description="A Bijoy to Unicode converter utility for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/codesigntheory/bijoytounicode",
    keywords='Bijoy Unicode Converter',
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    py_modules=["bijoytounicode"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing :: Linguistic"
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)

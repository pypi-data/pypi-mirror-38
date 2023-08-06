import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ausi",
    version="0.0.1",
    author="Markus Harrer",
    author_email="ausi@markusharrer.de",
    description="An Unified Software Integrator : A helper library that let's you output pandas DataFrames in all kinds of formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feststelltaste/ausi",
    packages=setuptools.find_packages(),
    install_requires=[
          'pandas',
          'matplotlib',
          'pygal'
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
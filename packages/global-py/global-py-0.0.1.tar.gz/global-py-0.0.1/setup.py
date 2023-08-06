import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="global-py",
    version="0.0.1",
    author="Frank Lu",
    author_email="frankz.lu@gmail.com",
    description="Make your python scripts globally accessible!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frankzl/globalpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points=
    {
        "console_scripts": ["globalpy = globalpy.global_setup:main"],
    },
)


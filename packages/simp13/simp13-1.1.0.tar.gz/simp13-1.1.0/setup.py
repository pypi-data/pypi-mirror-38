import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
#with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
#   long_description = f.read()
# This call to setup() does all the work
setup(
    name="simp13",
    version="1.1.0",
    description="Simple Utils Of simp13.com",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://simp13.com",
    author="Si Thu Phyo",
    author_email="createcodes155@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["imutils","six","numpy","opencv_contrib_python","progressbar2"],
    entry_points={
        "console_scripts": [
            
        ]
    },
)
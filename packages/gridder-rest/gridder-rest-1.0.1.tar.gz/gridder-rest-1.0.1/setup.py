from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="gridder-rest",
    version="1.0.1",
    description="REST-ful API for Gridder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/brzrkr/gridder-rest",
    author="Federico Salerno",
    author_email="itashadd+gridder@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    keywords="grid tile tileset image generator rest restful api",
    packages=find_packages(exclude=['test']),
    install_requires=['flask-restful', "flask", "webargs", "Pillow", 'gridder'],
    python_requires=">=3.2",
    project_urls={
        "Source": "https://gitlab.com/brzrkr/gridder-rest",
    },
)

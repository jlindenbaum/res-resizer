from distutils.core import setup

setup(
    name="res-resizer",
    version="0.4.0",
    author="Johannes Lindenbaum",
    author_email="johanneslindenbaum@gmail.com",
    packages=["resresizer"],
    url="http://pypi.python.org/pypi/res-resizer/",
    license="LICENSE",
    description="Resource resizer for Android and iOS",
    long_description=open("README.md").read(),
    install_requires=[
        "PIL>=1.1",
    ],
)
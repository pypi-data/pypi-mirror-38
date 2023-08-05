import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="godirect",
    version="0.9.7",
    author="Vernier Software and Technology",
    author_email="info@vernier.com",
    description="Library to interface with GoDirect devices via USB and BLE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vernierst",
    packages=setuptools.find_packages(),
    install_requires=[
        'vernierpygatt',
        'hidapi',
        'pexpect'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

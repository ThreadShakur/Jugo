import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="Jugo",
    version="1.0.4",
    author="Vadim Shpak",
    author_email="lansi_bro@bk.ru",
    description="Tool for easy communicating with MySQL/MariaDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThreadShakur/Jugo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymysql'
    ]
)
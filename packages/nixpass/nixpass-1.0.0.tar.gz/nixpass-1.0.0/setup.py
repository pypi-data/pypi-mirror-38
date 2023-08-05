import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nixpass",
    version="1.0.0",
    author="Shane Guymon",
    author_email="shane.eguymon@gmail.com",
    description="A cli password management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gatovato/nixpass",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ['nixpass = nixpass.nixpass:main']
        },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['pycrypto'],
    python_requires='>=3',
)

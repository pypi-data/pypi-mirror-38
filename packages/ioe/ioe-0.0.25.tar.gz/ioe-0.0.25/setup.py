import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ioe",
    version="0.0.25",
    author="Sergio Alonso",
    author_email="sergio@sergioalonso.es",
    description="The Python Internet of Energy Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sergioalonso/ioe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "jsonschema",
        "websockets",
        "websocket-client"
    ],
    include_package_data=True
)

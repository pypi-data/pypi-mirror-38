import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ioe",
    version="0.0.19",
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
        'python-jsonschema-objects @ git+https://github.com/sergio-alonso/python-jsonschema-objects@draft-handrews-json-schema-01#egg=python-jsonschema-objects-9.9.9.dev',
        "websockets",
        "websocket-client"
    ],
    dependency_links=[
    ],
    include_package_data=True
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inmation-api-client",
    version="0.2.3",
    author="Alexandr Sapunji",
    author_email="alexandr.sapunji@inmation.com",
    license='MIT',
    description="API client for system:inmation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://inmation.com",
    packages=setuptools.find_packages(),
    install_requires=[
          'websockets==6.0',
    ],
    classifiers=(
		"Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ),
)
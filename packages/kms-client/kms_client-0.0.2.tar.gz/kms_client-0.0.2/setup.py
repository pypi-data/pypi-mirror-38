from setuptools import setup, find_packages

setup(
    name="kms_client",
    version="0.0.2",
    author="Blake Lassiter",
    author_email="blakelass@gmail.com",
    description="A python implementation to get keys from KMS",
    url="https://github.com/balassit/kms_client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3"],
    include_package_data=True,
    zip_safe=False,
)

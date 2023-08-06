
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-util",
    version="0.1.0",
    author="Meng yangyang",
    author_email="mengyy_linux@163.com",
    description="Python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/hotbaby/py-util",
    install_requires=["pandas==0.19.0"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

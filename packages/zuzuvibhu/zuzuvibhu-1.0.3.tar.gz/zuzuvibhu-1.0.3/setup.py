import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name="zuzuvibhu",
    version="1.0.3",
    author="Vibhu Agarwal",
    author_email="vibhu4agarwal@gmail.com",
    description="Zuzu Package of Vibhu Agarwal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vibhu-Agarwal/zuzuvibhu",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='zuzu vibhu agarwal vibhuagarwal',
    install_requires=requirements
)

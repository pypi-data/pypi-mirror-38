import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='DSInterface',
    version='0.1rc2',
    description="A tiny python port of WPILib's driverstation class",
    url='https://github.com/frc5024/DSInterface',
    author='Evan Pratten',
    author_email='ewpratten@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['pynetworktables'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ),
)
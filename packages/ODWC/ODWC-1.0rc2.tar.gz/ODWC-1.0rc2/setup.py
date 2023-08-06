import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ODWC',
    version='1.0rc2',
    description='Open Driver Waypoint Coordinator',
    url='https://github.com/Ewpratten/ODWC',
    author='Evan Pratten',
    author_email='ewpratten@gmail.com',
    license='GPLv3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
)

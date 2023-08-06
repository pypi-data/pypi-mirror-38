import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='journaly',
     description='simple journal terminal program',
     author='unwoundclock',
     author_email='unwoundclock@gmail.com',
     version='0.1',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/lovebirdsnest/Journal.git",
     scripts=['journaly','README.md','LICENSE'],
     packages=setuptools.find_packages(),
     classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
 )

import setuptools

setuptools.setup(
        name='numberextractor',
        version='0.0.1',
        author='Feng Liu',
        author_email='feng3245@gmail.com',
        description='Simple package for extracting numbers',
        long_description='Extract computer uniform numbers from plain white background top down based on index',
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",]
        )

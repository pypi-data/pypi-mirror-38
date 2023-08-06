import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdndatapuller",
    version="1.0.2",
    author="Ykäz Mihar",
    author_email="zaky@femaledaily.com",
    description="Script Puller",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # entry_points={
    #     'console_scripts': 'halcyon=fdndatapuller.halcyon:main'
    # }
    scripts=['bin/halcyon']
)
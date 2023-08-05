import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="localizator",
    version="0.1.0",
    author="YogurtTheHorse",
    setup_requires=['pyyaml'],
    author_email="yogurt@yogurtthehor.se",
    description="Easy to use abstractions for localizing your python apps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yegorf1/localizator",
    packages=['localizator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django2-alexa",
    version="0.0.4",
    author="Tim Woocker & Malte Mosler",
    author_email="tim.woocker@googlemail.com",
    description="Django app for easily creating Amazon Alexa Skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timwoocker/django-alexa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_elo_rating",
    version="0.0.1",
    author="Sven Fritsch",
    author_email="sven@fritsch.io",
    description="ELO-Ratings for your django models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.fritsch.co/open-source/django_elo_rating",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.0"
    ],
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as r:
    req = r.read().splitlines()


setuptools.setup(
    name="SonoffBasic", # Replace with your own username
    version="0.0.2",
    author="Nicolas Golovaty",
    author_email="nicolascho2@gmail.com",
    description="basic package to control sonoff switches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devnicolasc/SonoffBasic",
    packages=setuptools.find_packages(),
    install_requires=req,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="walq",
    version="0.0.1",
    author="Pedro C. de Siracusa",
    author_email="pedrosiracusa@gmail.com",
    description="An very simple questionnaire-based chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrosiracusa/walQ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
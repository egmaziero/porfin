from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PorFin ChatBot",
    version="0.1.0",
    author="Erick Galani Maziero",
    author_email="egmaziero@gmail.com",
    description="A simple chatbot ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egmaziero/porfin_chatbot",
    project_urls={
        "Bug Tracker": "https://github.com/egmaziero/porfin_chatbot/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
)

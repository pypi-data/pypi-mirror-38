from pathlib import Path

import setuptools

from whohostwho import __version__, __author__


ROOT = Path(__file__).resolve().parent

setuptools.setup(
    name="whohostwho",
    version=__version__,
    author=__author__.split(" <")[0],
    author_email=__author__.split(" <")[1].strip("<>"),
    description="Project to fetch information about host and nameservers of a domain.",
    long_description=Path(ROOT / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Oprax/whohostwho",
    packages=setuptools.find_packages(),
    install_requires=["dnspython3", "progressbar2"],
    license="MIT",
    entry_points={"console_scripts": ["whohostwho = whohostwho:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
    ],
)

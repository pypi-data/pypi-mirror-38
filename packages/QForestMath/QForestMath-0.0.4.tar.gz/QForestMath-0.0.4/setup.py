import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QForestMath",
    version="0.0.4",
    author="Sashwat Anagolum",
    author_email="sashwat.anagolum@gmail.com",
    license="MIT License",
    description="A small math wrapper for QISkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SashwatAnagolum/DoNew/tree/master/qforest_math",
    packages=setuptools.find_packages(),
    requires="qiskit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="risc-translate",
    version="0.0.5",
    author="Kaya Çelebi",
    author_email="kayacelebi17@gmail.com",
    description="RISC-V translator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcelebi/riscv-translator",
    packages=setuptools.find_packages(),
    package_dir={'risc-translate':'.'},
    package_data={'risc-translate':['data/*.dat']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
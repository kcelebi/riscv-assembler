import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riscv-assembler",
    version="2.0.0",
    author="Kaya Çelebi",
    author_email="kayacelebi17@gmail.com",
    description="RISC-V assembler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcelebi/riscv-assembler",
    packages=setuptools.find_packages(),
    package_data={'riscv_assembler':['data/*.dat']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['bitstring==3.1.7'],
   # dependency_links = ["https://pypi.org/project/bitstring/"],
    python_requires='>=3'
)
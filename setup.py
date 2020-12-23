import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riscinterpreter", # Replace with your own username
    version="0.0.3",
    author="Kaya Çelebi",
    author_email="kayacelebi17@gmail.com",
    description="RISC-V interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcelebi/riscv-interpreter",
    packages=setuptools.find_packages(),
    package_dir={'riscinterpreter':'.'},
    package_data={'riscinterpreter':['data/*.dat']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
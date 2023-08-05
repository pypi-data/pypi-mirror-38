import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="removeOaExtension",
    version="0.0.6",
    author="João Campos",
    author_email="camposOnAi@gmail.com",
    long_description=long_description,
    description="Tool to remove vendor extension from OpenAPI documents",
    url="https://github.com/JoaoCamposFrom94/OpenAPI-extension-remover",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyYAML>=3.13',
    ],
    entry_points = {
        'console_scripts': ['removeOaExtension=implementation.main:main'],
    }
)

import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DSHIPconverter",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="observingClouds",
    author_email="",
    description="Scripts to converter DSHIP data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/observingClouds/DSHIPconverter",
    packages=setuptools.find_packages(),
    setup_requires=['setuptools-git-version'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["xarray>=0.11", "numpy", "netcdf4", "tqdm", "pandas"],
    entry_points={'console_scripts':
                    ['DSHIP2nc=DSHIPconverter.convert_DSHIP:main',
                     ]}
)

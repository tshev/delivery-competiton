import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delivery_competition", # Replace with your own username
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"delivery_competition": "delivery_competition"},
    packages=setuptools.find_packages(where="delivery_competition"),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "delivery_competition=delivery_competition:main"
        ]
    }
)

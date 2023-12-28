import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libage",
    version="0.0.6",
    author="moloch",
    author_email="875022+moloch--@users.noreply.github.com",
    description="Age compiled as a shared library and wrapped in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moloch--/libage",
    project_urls={
        "Bug Tracker": "https://github.com/moloch--/libage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
)

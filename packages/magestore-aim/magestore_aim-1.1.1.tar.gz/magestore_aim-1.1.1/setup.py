import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'magestore_aim'
packages = setuptools.find_packages(include=[package_name, "{}.*".format(package_name)])

setuptools.setup(
    name=package_name,
    version="1.1.1",
    author="Mars",
    author_email="mars@trueplus.vn",
    description="FIX return instance url",
    long_description=long_description + "\nThis module require fabric to run correctly.",
    long_description_content_type="",
    url="https://github.com/Magestore/go-environment",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
)

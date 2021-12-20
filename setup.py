from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in shiva_sakkthi_printers/__init__.py
from shiva_sakkthi_printers import __version__ as version

setup(
	name="shiva_sakkthi_printers",
	version=version,
	description="Handling entire flow of Shiva Sakkthi Printers",
	author="Thirvu Soft Private Limited",
	author_email="core@thirvusoft.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

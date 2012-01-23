from setuptools import setup, find_packages

version = '0.1'

setup(name='afs',
	version=version,
	packages=find_packages(exclude=['tests']),
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': [
			'afs = afs.main:main',
			],
		},
)

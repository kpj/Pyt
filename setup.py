from setuptools import setup, find_packages


def readme():
	with open('README.rst') as f:
		return f.read()

setup(
	name='pyt',
	version='0.0.1',
	description='A cli-based multi-protocol chat client',
	long_description=readme(),
	url='https://github.com/kpj/Pyt',
	author='kpj',
	author_email='kpjkpjkpjkpjkpjkpj@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	test_suite='nose.collector',
	tests_require=['nose'],
	scripts=['bin/pyt'],
	install_requires=['pyyaml', 'irc', 'tldextract']
)

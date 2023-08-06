from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='add-header-mv',
    version='0.3',
    author='tdkihrr',
    author_email='huanghezhao@outlook.com',
    url='https://github.com/tdkihrr/add-header-mv',
    keywords='tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    python_requires='>=3.4.0',
    description='Add header to files and move them',
    platforms='any',
    packages=[
        'hammal', 'hammal'
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'add-header-mv=hammal:main'
        ]
    }
)

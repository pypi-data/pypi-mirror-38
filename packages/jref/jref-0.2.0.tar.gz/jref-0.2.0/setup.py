import setuptools

from jref.version import version

with open('README.md') as readme:
    long_description = readme.read()

install_requires = []
with open('requirements.txt') as requirements:
    for line in requirements:
        requires = line.partition('#')[0]
        requires = line.strip()
        if requires:
            install_requires.append(requires)

setuptools.setup(
    name='jref',
    version=version,
    author=u'Jo\u00e3o Abecasis',
    author_email='joao@abecasis.name',
    description='JSON Reference and JSON Pointer implementations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/biochimia/python-jref',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    data_files=[('requirements', ['requirements.txt'])],
    install_requires=install_requires,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    entry_points={
        'console_scripts': [
            'jref=jref.__main__:main',
        ]
    },
)

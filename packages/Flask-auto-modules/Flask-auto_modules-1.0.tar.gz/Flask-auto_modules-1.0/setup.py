from setuptools import setup,find_packages

with open("./README.md", "r", errors='ignore') as fh:
    long_description = fh.read()

setup(
    name='Flask-auto_modules',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/Rinat93/flak-auto-modules',
    license='BSD',
    author='Zakirjanov Rinat',
    author_email='rinat643@gmail.com',
    description='Auto modules install',
    platforms='any',
    entry_points={
        'console_scripts':
            ['create = src.command:create_module']
    },
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
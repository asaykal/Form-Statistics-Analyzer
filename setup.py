from setuptools import setup, find_packages

setup(
    name='app',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'openpyxl',
        'matplotlib',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'app = app:app',
        ],
    },
)


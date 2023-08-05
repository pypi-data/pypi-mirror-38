from setuptools import setup, find_packages

setup(
    name='pydotfiles',
    version='0.0.0',
    description='Configuration-based python dotfiles manager',
    url='https://github.com/JasonYao/pydotfiles',
    author='Jason Yao',
    author_email='hello@jasonyao.com',
    packages=find_packages(),
    # package_data={'core': ['resources/*.ini']},
    scripts=['bin/dotfiles'],
    install_requires=[

    ],
    zip_safe=True,
    python_requires='>=3.6',
    extra_require={
        'dev': [
            'pyest',
            'pytest-pep8',
            'pytest-cov'
        ]
    }
)

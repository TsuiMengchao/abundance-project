from setuptools import setup, find_packages

setup(
    name='abundance',
    version='bate 0.0.1',
    author='mcx',
    author_email='tsuimengchao@gmail.com',
    description='A Python framework',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    url='https://abundance.zhaohaoyue.love',
    packages=find_packages(),
    install_requires=[
        'yaml',
        'json',
        'Pillow',
    ],
    extras_require = {
        'full': ['scipy', 'pillow', 'colorthief']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Documentation': 'https://doc.abundance.zhaohaoyue.love',
        'Source Code': 'https://github.com/tsuimengchao/abundance',
        'Bug Tracker': 'https://github.com/tsuimengchao/abundance/issues',
    },
    python_requires='>=3.6',
)
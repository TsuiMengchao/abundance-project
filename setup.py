from setuptools import setup, find_packages

setup(
    name='abundance',
    version='0.0.1-beta',  # 确保版本号与 pyproject.toml 一致
    author='tsuimengchao',
    author_email='tsuimengchao@gmail.com',
    description='A Python framework',
    long_description=open('README_zh.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    url='https://abundance.zhaohaoyue.love',
    packages=find_packages(),
    install_requires=[
        'pycryptodome (>=3.21.0,<4.0.0)',
        'pytz (>=2024.2,<2025.0)',
        'python-magic (>=0.4.27,<0.5.0)',
        'pandas (>=2.2.3,<3.0.0)',
        'openpyxl (>=3.1.5,<4.0.0)',
        'redis (>=5.2.1,<6.0.0)',
        'cryptography (>=44.0.0,<45.0.0)',
        'psutil (>=6.1.1,<7.0.0)',
        'validators (>=0.34.0,<0.35.0)',
        'pydantic (>=2.10.4,<3.0.0)',
        'requests (>=2.32.3,<3.0.0)',
        'pyjwt (>=2.10.1,<3.0.0)',
    ],
    extras_require = {
        'full': ['scipy', 'pillow', 'colorthief']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 确保许可证信息准确
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Documentation': 'https://doc.abundance.zhaohaoyue.love',
        'Source Code': 'https://github.com/tsuimengchao/abundance',
        'Bug Tracker': 'https://github.com/tsuimengchao/abundance/issues',
    },
    python_requires='>=3.11',  # 确保 Python 版本要求与 pyproject.toml 一致
)
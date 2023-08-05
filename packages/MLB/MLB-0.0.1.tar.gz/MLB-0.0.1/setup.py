from setuptools import setup
from setuptools import find_packages

setup(
    name='MLB',
    version='0.0.1',
    description='hogehoge',
    author='mucunwuxian',
    author_email='taketo_kimura@micin.jp',
    url='https://github.com/micin-jp/MLB',
    download_url='',
    install_requires=['numpy==1.13.3',
                      'pandas>=0.21.0',
                      'scikit-learn>=0.19.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    keywords='hogehoge',
    packages=find_packages()
)

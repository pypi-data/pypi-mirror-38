from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='grafos',
    version='1.0.1',
    description='Ferramenta de algoritmos de Teoria e Modelagem de Grafos',
    url='http://github.com/gfviegas/grafos',
    author='Gustavo Viegas, Lucas Duarte',
    author_email='gustavo.viegas@ufv.br, lucas.duarte@ufv.br',
    license='Apache',
    packages=['grafos', 'memoize'],
    install_requires=[
        'numpy'
    ],
    setup_requires=[
        'pytest-runner',
        'sphinx_rtd_theme',
        'sphinxcontrib-fulltoc'
    ],
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=False,
    download_url='https://github.com/gfviegas/grafos/archive/1.0.tar.gz'
)

import setuptools
from pathlib import Path

readme_path = Path('./README')

setuptools.setup(
    name='plpy_ext',
    version='0.0.8',
    author='Filantus',
    author_email='filantus@mail.ru',
    url='https://pypi.org/project/plpy-ext/',
    description='Some extensions for plpython3u.',
    long_description=readme_path.read_text(),
    py_modules=['plpy_ext'],
    packages=setuptools.find_packages(),
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
)

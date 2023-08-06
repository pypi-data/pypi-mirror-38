from setuptools import setup

description = 'Some extensions for plpython3u.'

setup(
    name='plpy_ext',
    version='0.0.5',
    author='Filantus',
    author_email='filantus@mail.ru',
    description=description,
    long_description=description,
    py_modules=['plpy_ext'],
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
)

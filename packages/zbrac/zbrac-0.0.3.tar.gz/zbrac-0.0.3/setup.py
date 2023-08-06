import setuptools

setuptools.setup(
    name='zbrac',
    version='0.0.3',
    #packages=['XlsxWriter', 'openpyxl', 'PyQt5','urllib3','PyQt5-sip'],
	packages=['zbrac'],
    url='https://github.com/seyhunsaral/zbrac',
    license='GNU Public Licence',
    author='Ali Seyhun Saral, Anna Marie Schroeter',
    author_email='seyhunsaral@gmail.com, schroeter@coll.mpg.de',
    description='A language tool for zTree',
    install_requires=['openpyxl>=2.5.8','PyQt5>=5.11.3','PyQt5-sip>=4.19.13','urllib3>=1.24.1','XlsxWriter>=1.1.1'],
    entry_points = {'console_scripts': ['zbrac=zbrac.start:main'],},
    zip_safe=False
)

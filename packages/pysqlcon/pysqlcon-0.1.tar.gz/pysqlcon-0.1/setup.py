from setuptools import setup, find_packages
 
setup(name='pysqlcon',
      version='0.1',
      url='https://github.com/kudzaitsapo/pysqlcon',
      license='MIT',
      author='Kudzai Tsapo',
      author_email='kudzai@charteredsys.com',
      description='Easy execution of sql statements and stored procedures on MSSQL database',
      packages=find_packages(exclude=['test.py']),
      long_description=open('README.md').read(),
      zip_safe=False)
from setuptools import setup

setup(

    name="web_assist",
    version='0.0.1',
    url='https://github.com/pytholabsbot1/web_assist',
    author='Pytholabs',
    author_email='info@pytholabs.com',  
    description='provides multiple tools to work with webapps',
    py_modules=['webAssist'],
    package_dir={'':'src'},

    install_requires=[
          'requests',
      ],

    )

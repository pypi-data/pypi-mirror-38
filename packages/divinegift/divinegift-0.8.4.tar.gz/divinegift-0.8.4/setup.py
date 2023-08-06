from setuptools import setup, find_packages 

setup(name='divinegift',
      version='0.8.4',
      description='It is a Divine Gift',
      long_description='The most useful package for you, young s7_it programer :)',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent", ],
      keywords='s7_it',
      url='https://github.com/Malanris/DivineGift.git',
      author='Malanris',
      author_email='admin@malanris.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=['sqlalchemy', 'requests', 'mailer'],
      include_package_data=True,
      zip_safe=False)
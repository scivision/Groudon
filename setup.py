#!/usr/bin/env python
install_requires=['pillow','simplejson']
tests_require=['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='Groudon',
      packages=find_packages(),
      description='',
      version='0.1.0',
      url='https://github.com/scivision/Groudon',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 3',],
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plot':['matplotlib','seaborn',],},
      python_requires='>=2.7',
   )

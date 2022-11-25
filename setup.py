from setuptools import setup, find_packages

setup(name='mergegoogledocwithipynb',
      version='0.1.1',
      description='merge google doc with ipynb',
      url='https://github.com/gwubc/MergeGoogleDocWithIpynb/blob/master/README.ipynb',
      author='gw',
      author_email='',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'nbformat',
          'requests',
          'markdownify',
      ],
      zip_safe=False)

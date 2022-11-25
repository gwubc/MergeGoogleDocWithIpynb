from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(name='mergegoogledocwithipynb',
      version='0.1.2',
      description='merge google doc with ipynb',
      long_description=long_description,
      long_description_content_type='text/markdown',
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

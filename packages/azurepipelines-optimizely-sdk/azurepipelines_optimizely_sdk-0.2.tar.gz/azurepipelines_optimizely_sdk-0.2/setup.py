from setuptools import setup

setup(name='azurepipelines_optimizely_sdk',
      version='0.2',
      description='SDK for optimizely integration',
      url='http://github.com/microsoft/azurepipelines-optimizely-sdk',
      author='Ajay Yadav',
      author_email='ajya@microsoft.com',
      license='MIT',
      packages=['azurepipelines_optimizely_sdk'],
      install_requires=[
          'optimizely-sdk',
      ],
      zip_safe=False)

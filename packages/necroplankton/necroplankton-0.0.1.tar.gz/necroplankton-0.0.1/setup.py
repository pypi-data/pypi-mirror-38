from setuptools import setup, find_packages

setup(name='necroplankton',
      version='0.0.1',
      description='tool set',
      author='necroplankton',
      author_email='necroplankton@rainy.me',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.6',
      ],
      python_requires='>=3.6',
      license="MIT Licence",
      packages=find_packages(),
      install_requires=["requests"]
      )

from setuptools import setup, find_packages

setup(name='hindikosh',
      version='0.0.1',
      description='Hindi corpus reader',
      long_description='Hindi corpus reader',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='hindi corpus reader tokenizer',
      url='https://github.com/daksh95/hindi-corpus',
      author='Karishnu Poddar',
      author_email='karishnu@gmail.com',
      license='MIT',
      packages=['hindikosh'],
      install_requires=[
          'markdown','numpy','pydub'
      ],
      include_package_data=True,
      zip_safe=False)

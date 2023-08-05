from setuptools import setup

setup(
  name = 'deepchar',
  packages = ['deepchar'],
  version = '0.1',
  description = 'Transliteration with sequence-to-sequence models and transfer learning',
  author = 'ModelFront',
  author_email = 'deepchar@modelfront.com',
  url = 'https://github.com/deepchar/deepchar',
  download_url = 'https://github.com/deepchar/deepchar/archive/0.1.tar.gz',
  keywords = ['natural language processing', 'text', 'translation', 'transliteration', 'translit'],
  license='MIT',
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

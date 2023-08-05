# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['phsic']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.2.8,<0.3.0',
 'gensim>=3.6,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=0.23.4,<0.24.0',
 'scipy>=1.1,<2.0',
 'sklearn>=0.0.0,<0.0.1',
 'statsmodels>=0.9.0,<0.10.0',
 'tensorflow-hub>=0.1.1,<0.2.0',
 'tensorflow>=1.7,<2.0']

entry_points = \
{'console_scripts': ['phsic = phsic.app:main']}

setup_kwargs = {
    'name': 'phsic-cli',
    'version': '0.1.0',
    'description': 'Pointwise Hilbert–Schmidt Independence Criterion (PHSIC)',
    'long_description': '# Pointwise Hilbert窶鉄chmidt Independence Criterion (PHSIC)\n\nCompute *co-occurrence* between two objects utilizing *similarities*.\n\nFor example, given consistent sentence pairs:\n\n| X                                                            | Y                  |\n| ------------------------------------------------------------ | ------------------ |\n| They had breakfast at the hotel.                             | They are full now. |\n| They had breakfast at ten.                                   | I\'m full.          |\n| She had breakfast with her friends.                          | She felt happy.    |\n| They had breakfast with their friends at the Japanese restaurant. | They felt happy.   |\n| He have trouble with his homework.                           | He cries.          |\n| I have trouble associating with others.                      | I cry.             |\n\nPHSIC can give high scores to consistent pairs in terms of the given pairs:\n\n| X                                            | Y                     | score  |\n| -------------------------------------------- | --------------------- | ------ |\n| They had breakfast at the hotel.             | They are full now.    | 0.1134 |\n| They had breakfast at an Italian restaurant. | They are stuffed now. | 0.0023 |\n| I have dinner.                               | I have dinner again.  | 0.0023 |\n\n## Installation\n\n```\n$ pip install phsic\n```\n\nThis will install `phsic` command to your environment:\n\n```\n$ phsic --help\n```\n\n## Basic Usage\n\nDownload pre-trained wordvecs (e.g. fasttext):\n\n```\n$ wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/crawl-300d-2M.vec.zip\n$ unzip crawl-300d-2M.vec.zip\n```\n\nPrepare dataset:\n\n```\n$ TAB="$(printf \'\\t\')"\n$ cat << EOF > train.txt\nThey had breakfast at the hotel.${TAB}They are full now.\nThey had breakfast at ten.${TAB}I\'m full.\nShe had breakfast with her friends.${TAB}She felt happy.\nThey had breakfast with their friends at the Japanese restaurant.${TAB}They felt happy.\nHe have trouble with his homework.${TAB}He cries.\nI have trouble associating with others.${TAB}I cry.\nEOF\n$ cut -f 1 train.txt > train_X.txt\n$ cut -f 2 train.txt > train_Y.txt\n$ cat << EOF > test.txt\nThey had breakfast at the hotel.${TAB}They are full now.\nThey had breakfast at an Italian restaurant.${TAB}They are stuffed now.\nI have dinner.${TAB}I have dinner again.\nEOF\n$ cut -f 1 test.txt > test_X.txt\n$ cut -f 2 test.txt > test_Y.txt\n```\n\nThen, train and predict:\n\n```\n$ phsic train_X.txt train_Y.txt --kernel1 Gaussian 1.0 --encoder1 SumBov FasttextEn --emb1 crawl-300d-2M.vec --kernel2 Gaussian 1.0 --encoder2 SumBov FasttextEn --emb2 crawl-300d-2M.vec --limit_words1 10000 --limit_words2 10000 --dim1 3 --dim2 3 --out_prefix toy --out_dir out --X_test test_X.txt --Y_test test_Y.txt\n$ cat toy.Gaussian-1.0-SumBov-FasttextEn.Gaussian-1.0-SumBov-FasttextEn.3.3.phsic\n1.134489336180434238e-01\n2.320408776101631244e-03\n2.321869174772554344e-03\n```\n\n## Citation\n\n```\n@InProceedings{D18-1203,\n  author = \t"Yokoi, Sho\n        and Kobayashi, Sosuke\n        and Fukumizu, Kenji\n        and Suzuki, Jun\n        and Inui, Kentaro",\n  title = \t"Pointwise HSIC: A Linear-Time Kernelized Co-occurrence Norm for Sparse Linguistic Expressions",\n  booktitle = \t"Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",\n  year = \t"2018",\n  publisher = \t"Association for Computational Linguistics",\n  pages = \t"1763--1775",\n  location = \t"Brussels, Belgium",\n  url = \t"http://aclweb.org/anthology/D18-1203"\n}\n```\n',
    'author': 'Sho Yokoi',
    'author_email': 'yokoi@ecei.tohoku.ac.jp',
    'url': 'https://github.com/cl-tohoku/phsic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

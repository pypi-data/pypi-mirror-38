# Compression Techniques for sparse binary data

## In Development

## Prerequisites ##
* Python 2.7 or higher
* [NumPy](http://numpy.org)
* [scikit learn](https://scikit-learn.org/stable/)
* Libraries: [Pickle], [random], [re]

## Usage
```
from BinHash import hasher
corpus = 'path_to_the_folder_containing_documents'
d = 10000
k = 500
myhasher = hasher(corpus, d, k)
sample_text = "this is a sample text"
sample_hash = myhasher.hash_text(sample_text)
```

## Citation

Please cite these papers in your publications if it helps your research 
```
@inproceedings{DBLP:conf/pakdd/PratapSK18,
  author    = {Rameshwar Pratap and
               Ishan Sohony and
               Raghav Kulkarni},
  title     = {Efficient Compression Technique for Sparse Sets},
  booktitle = {Advances in Knowledge Discovery and Data Mining - 22nd Pacific-Asia
               Conference, {PAKDD} 2018, Melbourne, VIC, Australia, June 3-6, 2018,
               Proceedings, Part {III}},
  pages     = {164--176},
  year      = {2018},
  crossref  = {DBLP:conf/pakdd/2018-3},
  url       = {https://doi.org/10.1007/978-3-319-93040-4\_14},
  doi       = {10.1007/978-3-319-93040-4\_14},
  timestamp = {Tue, 19 Jun 2018 09:13:55 +0200},
  biburl    = {https://dblp.org/rec/bib/conf/pakdd/PratapSK18},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}


@inproceedings{compression,
 author    = {Rameshwar Pratap and
               Raghav Kulkarni and
		Ishan Sohony},
  title     = {Efficient Dimensionality Reduction for Sparse Binary Data},
  booktitle = {IEEE International Conference on BIG DATA, Accepted},
  year      = {2018}
}
```

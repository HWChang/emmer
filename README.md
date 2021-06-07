![conda](https://anaconda.org/bioconda/piemmer/badges/installer/conda.svg)
![pypi](https://img.shields.io/pypi/v/piemmer?style=flat-square)
![conda version](https://anaconda.org/bioconda/piemmer/badges/version.svg)
![platforms](https://anaconda.org/bioconda/piemmer/badges/platforms.svg)
![license](https://anaconda.org/bioconda/piemmer/badges/license.svg)

# PIEMMER: Simplify the Input for Principal Component Analysis

EMMER, which stands for Entropy-based Method for Microbial Ecology Research, is a feature selection algorithm that reduces the number of measurements in a matrix while allowing this new matrix to retains a similar data distribution on a Principal Component Analysis (PCA) plot (see Fig. 1; [view figure](https://drive.google.com/file/d/1m2O658NZMInmYYlyI9AdUuz2hbg14U6X/view?usp=sharing)). We named this algorithm EMMER because it was originally developed to processing microbiota and microbiome datasets. Later, we realize this algorithm has a wider application because the shared mathematical procedure between EMMER algorithm and PCA

PIEMMER is a python package that implement EMMER algorithm.

![Figure 1. What EMMER can do?](https://drive.google.com/uc?id=1m2O658NZMInmYYlyI9AdUuz2hbg14U6X)
**Fig 1. What EMMER can do?**

## About
- **Version:** 1.0.5
- **License:** BSD 3-Clause License
- **Developer/Maintainer:** Hao-Wei Chang (email: emmer.man42@gmail.com)
- **Citation:** H.-W. Chang et al., Gut microbiome contributions to altered metabolism in a pig model of undernutrition. (2021) _Proc Natl Acad Sci U S A._ **118**, e2024446118.
  1. [Main article; how to use EMMER in microbiota/microbiome studies](https://www.pnas.org/content/118/21/e2024446118)
  2. [SI Appendix; how EMMER algorithm works](https://www.pnas.org/content/pnas/suppl/2021/05/14/2024446118.DCSupplemental/pnas.2024446118.sapp.pdf)


## Download and Usage
Option 1 - Anaconda
```bash
conda install -c bioconda piemmer
```

Option 2 - Pypi
```bash
pip install piemmer
```

Option 3 - Download from github
```bash
cd where_you_what_to_store_your_file
git clone https://github.com/HWChang/emmer.git

# see a folder name emmer appear under where_you_what_to_store_your_file
mv emmer piemmer
```

Get the location of example files that were included in the package
```bash
import pkg_resources
```
```python3
import pkg_resources
DATA_PATH = pkg_resources.resource_filename('piemmer', 'data/')
DATA_PATH
```

Run piemmer
```bash
cd where_your_what_to_put_the_output_files
python3 -m piemmer.harvest -g
python3 -m piemmer.bake -g
```

**Please refer to the [wiki](https://github.com/HWChang/emmer/wiki) page for detailed information about download, dependency, and tutorial.**

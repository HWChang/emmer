# EMMER: Simply the Input for Principal Component Analysis

## What is EMMER?
EMMER, which stands for Entropy-based Method for Microbial Ecology Research, is **a feature selection algorithm that reduces the number of measurements in a matrix while allowing this new matrix to retains a similar data distribution on a PCA plot** (see figure illustration below or [here](https://drive.google.com/file/d/1m2O658NZMInmYYlyI9AdUuz2hbg14U6X/view?usp=sharing)).

![Figure 1. What EMMER can do?](https://drive.google.com/uc?id=1m2O658NZMInmYYlyI9AdUuz2hbg14U6X)

We named this algorithm EMMER, which stands for Entropy-based Method for Microbial Ecology Research, because we originally developed this algorithm to processing data from microbiota/microbiome studies. Later we realize this algorithm has wider application because the EMMER algorithm and PCA share the same mathematical procedure.


## About
- **Version:** 1.0
- **License:** BSD 3-Clause License
- **Developer/Maintainer:** Hao-Wei Chang (email: emmer.man42@gmail.com)
- **Citation:** H.-W. Chang et al., Gut microbiome contributions to altered metabolism in a pig model of undernutrition. (2021) _Proc Natl Acad Sci U S A._ **118**, e2024446118.
  1. [Main article; how to use EMMER in microbiota/microbiome studies](https://www.pnas.org/content/118/21/e2024446118)
  2. [SI Appendix; how EMMER algorithm works](https://www.pnas.org/content/pnas/suppl/2021/05/14/2024446118.DCSupplemental/pnas.2024446118.sapp.pdf)


## Download
```bash
cd where_you_want_to_store_the_script
git clone https://github.com/HWChang/emmer.git
```

You will see a new folder called ```emmer``` appear in after ```where_you_want_to_store_the_script``` the download.


## Usage
Go to the directory where you store ```emmer```

```bash
cd where_you_want_to_store_the_script
```

Analyze your data with EMMER usually takes three steps. First, we analyze your input data with the default setting and see if it works. Then, we can do a parameter sweep to optimize the setting. After parameter sweep, we reanalyze your input data with the optimized setting.

We will use ```emmer.harvest``` module for the first and the third step, and use ```emmer.bake``` module for parameter sweep and additional analyses. To learn more about different arguments in each of those modules, please use the following command:

```bash
python3 -m emmer.harvest -g
python3 -m emmer.bake -g
```

An example input for EMMER can be found under

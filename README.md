## EMMER: a feature selection algorithm for Principal Component Analysis

### What is EMMER?
EMMER, which stands for Entropy-based Method for Microbial Ecology Research, is **a feature selection algorithm that reduces the number of measurements in a matrix while allowing this new matrix to retains a similar data distribution on a PCA plot** (see figure illustration below or [here](https://drive.google.com/file/d/1m2O658NZMInmYYlyI9AdUuz2hbg14U6X/view?usp=sharing)).

![Figure 1. What EMMER can do?](https://drive.google.com/uc?id=1m2O658NZMInmYYlyI9AdUuz2hbg14U6X)


We named this algorithm EMMER, which stands for Entropy-based Method for Microbial Ecology Research, because we originally developed this algorithm to processing data from microbiota/microbiome studies. Later we realize this algorithm has wider application because the EMMER algorithm and PCA share the same mathematical procedure.


### About
- **Version:** 1.0
- **Developer/Maintainer:** Hao-Wei Chang (email: emmer.man42@gmail.com)
- **Citation:** H.-W. Chang et al., Gut microbiome contributions to altered metabolism in a pig model of undernutrition. (2021) _Proc Natl Acad Sci U S A._ **118**, e2024446118.


### Download
```bash
cd where_you_want_to_store_the_script
git clone https://github.com/HWChang/emmer.git
```


### Usage
```bash
cd where_you_want_to_store_the_script
python3 -m emmer.harvest -g
python3 -m emmer.bake -g
```


### License
BSD 3-Clause License

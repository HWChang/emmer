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

EMMER expect csv file(s) looks like files in:
```bash
emmer/data/data_dir_3/
```

Each csv file store a input data matrix, where each row is a sample and each column is a measurements. Each cell in the matrix is a number. Please note EMMER expect the matrix to have row names and column names. Please do not include "__" (double underscore) in your row names.

After prepare all your input file, you can run EMMER with the default setting

```bash
python3 -m emmer.harvest -i emmer/data/data_dir_3 -f 'HardFilter' -u 2 -l 2 -t 2 -d 0.001 -z 0.33 -r
```

In this command:
1. ```-i```: Input directory that contains one or many csv files or a path to specific csv file.
2. ```-r```: Convert the input data matrix to relative abundance. Number in the row will be divided by the row sum.
3. ```-f```: Filter data before run EMMER. Currently, EMMER offers two options ```'HardFilter'``` or ```'None'```. Please use ```python3 -m emmer.harvest -g``` to get more information on those two options.
4. ```-d```, ```-z```: Additional arguments when choose to use  ```-f 'HardFilter'```. ```-d``` determines the detection limit. Any number low the limit of detection will be set as 0. ```-z``` should be a number less than 1 but greater than 0. This number represents the maximum fraction of element in each column of your input matrix that can be zero. Any column (measurements) contains more 0 than ```-z``` will be remove before running EMMER.
5. ```-u```, ```-l```, ```-t```: Parameters for feature selection. Briefly, ```-u``` and ```-l``` set the upper and lower limit when choosing information-rich features. ```-t``` many times a feature need to be nominate as information-rich feature in jackknife subsampling to be included in the final list of information-rich features. Please note EMMER expect a integer for ```-t``` that is less than the number of row in your input data matrix.

  **Note:** When using ```-r```, ```-f 'HardFilter'```, ```-d```, and ```-z``` together in your command, the order of execution when running EMMER is: ```-r``` -> ```-f 'HardFilter'``` -> ```-d``` -> ```-z```

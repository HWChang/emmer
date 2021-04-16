# EMMER
Entropy-based Method for Microbial Ecology Research (EMMER)


## About
Version: 0.9.1 (under development)

Description: Python package (pre-deploy)

Key features:
1. Applying SVD to calculate the transformation matrix and unlock potential applications of EMMER
2. Flexible setting for data filter and information-rich feature selection threshold
3. Introducing MinDataLostFilter
4. Generating transformation and scaler for projecting samples onto PCA spaces
5. Adding tests and corresponding datasets
6. Introducing sanityCheck option when working on multiple files and including options to visualizing sanityCheck result when running on local computer
7. Introducing retrospect module for additional test and plot options
8. Limit the number of information-rich to avoid potential overfitting problem
9. Provide advise on threshold setting
10. Packaging EMMER (v0.8c6)

## Usage
### Expected input and output files:

**Requirement:**

At least one csv file. Expect to have column headers and row names. Expect a numeric matrix. Each row represents a sample and each column represents a feature.
The data matrix should be numeric.


**Output:**
1. List of information-rich feature. When set Quick Look Mode off, EMMER will also reports the reproducibility for information-rich feature calling
2. Coordinates of each samples in the abstract PCA space
2. Transformation matrix and scaler for user to project new observations onto the existing PCA space

### How to run EMMER
Download the scripts from this deposit and run in your local computer

```bash
cd where_you_store_those_scripts

python3 -m emmer.harvest.py -i <dir_that_store_your_csv_file(s)_or_specific_csv_file> \
                            -o <a_string_that_will_attach_to_all_of_your_output_files___optional> \
                            -d <detection_limit___optional> \
                            -f <filter> \
                            -z <zero_tolerance_level_used_for_hardFilter> \
                            -q <quick_look_mode___optional> \
                            -u <upper_threshold_for_infoRich_calling> \
                            -l <lower_threshold_for_infoRich_calling> \
                            -p <if_you_want_to_plot_the_result___optional> \
                            -s <if_you_want_to_generate_plots_for_sanity_check___optional> \
```


**Quick demo on local computer**
```bash
cd where_you_store_those_scripts

python3 -m emmer.harvest.py emmer.py -i data/data_dir_3/ \
                                     -f 'HardFilter' \
                                     -d 0.001 \
                                     -z 0.33 \
                                     -u 2 \
                                     -l 2 \
                                     -t 2 \
                                     -r
                                     -p
```
-f: choose data filter. We choose to use Hardfilter in this example.

-d: detection limit. We set the detection limit at 0.001, which is equivalent of 0.1% in relative abundance.

-z: zero tolerance. Columns with more than 1/3 of its elements contain a value that is less then the detection limit will be filtered out before EMMER feature reduction.

-u: upper threshold of information-rich feature calling. In this case, we set at the upper threshold at 2 standard deviations.

-l: lower threshold of information-rich feature calling. In this case, we set at the lower threshold at 2 standard deviations.

-t: a feature needed to be pick up more than 2 times during the jackknift subsampling step before being included in the list of information-rich features

-r: covert count (input data) into factional abundance before filtering data and EMMER feature

-p: visualize feature reduction result in PCA plot. Feel free to rotate the 3D PCA plot when it pop up. This interactive plot allows the user to choose the best angle to present his/her data. The plot will automatically be saved as a 300 dpi pdf file after you close the interactive window.


```bash
cd where_you_store_those_scripts

python3 -m emmer.harvest.py emmer.py -i my_metagenomic_tpm_data/ \
                                     -f 'None' \
                                     -u 2 \
                                     -l 2 \
                                     -t 2 \
                                     -p
```
In this example, user wish to applied EMMER on a filtered metagenomics dataset. Because the user already filter the data, args.f (-f) is set at 'None' to prevent additional data filtering.  

## Future updates
### Plans for v0.9 update:
1. Depreciated MinDataLostFilter -> OK
2. Automatically generate notebook when running emmer.bake  -> OK (permanova)
3. Organize data for test and tutorial
4. Automatically remove files generated during testing -> OK
5. Issue warning/input before initiate test -> OK
6. Extend notebook to cover tests
7. (0.9.1) Allow cor = T (emmer.harvest: OK; emmer.bake: not OK)

### Objectives for v1:
1. Official release of EMMER on github

## TODO:
1. For 3D plot: export azimuth and elevation information
# https://stackoverflow.com/questions/23424282/how-to-get-azimuth-and-elevation-from-a-matplotlib-figure

2. PCoA
# https://www.geeksforgeeks.org/ml-principal-component-analysispca/

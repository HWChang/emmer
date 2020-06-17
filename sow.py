#!/usr/bin/env python3

from .main.basic.read import GetFiles, RawDataImport
from .toolbox.technical import addElementsInList, dualAssignment

import pandas as pd
import argparse
import os

"""
A collection of data cleaning method before submit the data to EMMER
"""

##==0==##


##==1==##
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type = str,
                        help = 'Input directory that contains one or many csv files or a path to specific csv file. Expect to have column headers and row names. Each row represents a sample and each column represents a feature.')
    #parser.add_argument('-m', '-method', type = str, choices = ['DecomposeColumn']
    #                    help = 'XXXXXX')
    parser.add_argument('-m', '-method', choices = ['DecomposeColumn', 'MergeFilesByGroup'],
                        help = 'choose method. [DecomposeColumn] XXX.')


    parser.add_argument('-o', type = str,
                        help = 'Tag for the all output file names.')
    parser.add_argument('-s', '-separate', type = str,
                        help = 'Sep XXXXXX')

    parser.add_argument('-k', '-key', type = int,
                        help = 'Location; starts with 0. Row name in the merged files')
    parser.add_argument('-v', '-value', type = int,
                        help = 'Location; starts with 0. value fill in the in the merged matrix')

    args = parser.parse_args()


##==2==##
##--1--##
    if args.m == 'MergeFilesByGroup':
        


##--2--## DecomposeColumn
    if agrs.m == 'DecomposeColumn':

    ## for test:
    #  python3 pretreatment.py -i data/pretreatment_data_dir_1/ -o 'CAZ' -s '-'
        if args.o:
            print(f'Output file tag: {args.o}\n')
            output_file_tag = args.o
        else:
            print(f'No output file tag.\n')
            output_file_tag = ''

        ## handle output dir
        current_wd = os.getcwd()
        processed_dir = os.path.join(current_wd, 'processed')
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)


        input_dir = os.path.join(current_wd, args.i)
        input = GetFiles(input_dir)

        for f in range(len(input.input_files)):
            file = RawDataImport(input.input_files[f])
            file.readCSV()
            input_df = file.data
            decompose_col_dict = dualAssignment(input_df, sep = args.s)

            transformed_df = pd.DataFrame.from_dict(decompose_col_dict)
            transformed_df.index = file.sample_id

            output_file_name = os.path.join(processed_dir, file.basename.replace(".csv", "")) + output_file_tag + ".csv"
            transformed_df.to_csv(output_file_name)

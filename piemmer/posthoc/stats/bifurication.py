#!/usr/bin/env python3

from ...toolbox.technical import *
from ...main.basic.read import RawDataImport, RetrospectDataImport, GetFiles
from ...posthoc.visual.viewer import Projection
from ...troubleshoot.err.error import *

import statsmodels.api as sm
import pandas
import numpy
import math

"""
Support emmer.bake Bifurication mode

identify information-rich features that help to differentiate different groups on the PCA space.
"""

class BifuricationArgs:
    """
    Take common arguments for Bifurication modes when running bake modules

    Objective: so we can test and use @

    Argument:
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        second_chance -- Type: boolean
        current_wd -- Type: str
                      current working directory

    Attributes:
        list_of_info_rich -- Type: list
        input_files -- Type: list
                       List of input file with full path
    """
    def __init__(self, args, current_wd, suppress):

        # handle args.p (e.g.: information_rich_features_summary.csv)
        try:
            if args.p:
                 print(f'Input -p: {args.p}')
                 repro = RetrospectDataImport(file_name = os.path.join(current_wd, args.p), type = 'reproducibility')
            else:
                 raise Error(code = '12')
        except Error as e:
            raise ErrorCode12(suppress = suppress) from e
        self.list_of_info_rich = list(repro.reproducibility.index)

        # handle args.i (e.g. output/filtered_data/)
        try:
            if args.i:
                self.input_files = GetFiles(os.path.join(current_wd, args.i)).input_files

                if len(self.input_files) < 2:
                    raise Error(code = '21')
            else:
                raise Error(code = '21')
        except Error as e:
            raise ErrorCode21(suppress = suppress)

        def getArgsN(self):
            if self.args.n:
                self.normalize = True
            else:
                self.normalize = False

def linearRegressionPVal(target, data, silence_intersect = True):
    """
    Purpose:
        Get p values for each correlations coefficients and intercept in the linear
        regression model.

    Arguments:
        target -- Type: pandas.DataFrame
                  One column. The number of row corresponding to the number of sample.
                  Expect integer or float for each elements.
        data -- Type: pandas.DataFrame
                The number of column corresponding to the number of information-rich
                features. The number of row corresponding to the number of samples.
                Expect integer or float for each elements.
        silence_intersect -- Type: boolean
                             Report the p value for intersect or not. Please note that
                             when set silence_intersect = False, this function will still
                             calculate the linear regression model that has an intersect.


    Reture:
        pvalues -- Type: pandas.DataFrame
                   Row names (pandas.DataFrame.index) are the name of the feature

    Technical:
        Note that it is difficult to get this pieces of information from sklearn.linear_model
        The alternative is to use statsmodels package to conduct linear regression because
        it is easier to get that information from statsmodels output.
    """
    # consider intersect in the regression model. same as LinearRegression(fit_intercept=True)
    data_ = sm.add_constant(numpy.array(data))
        # now the first column of data_ is the intercept

    model = sm.OLS(target, data_)
    result = model.fit()

    pvalues = pandas.DataFrame(result.pvalues, columns = ['pval'])
    pvalues.index = ['intercept'] + list(data.columns)

    if silence_intersect == True:
        pvalues = pvalues.drop(pvalues.index[0])

    return(pvalues)


class DifferentiatingFeatures:
    """
    Purpose:
        Determine features that contribute to the significant difference of groups in
        PCA space.

    Arguments:
        Projection_class -- Type: Projection class object

        From Projection_class, DifferentiateGroup class requires:
        Projection_class.spec_cleaned_data -- Type: numpy.narray
                                              row: samples
                                              column: features
                                                      Although not restricted to specific set of
                                                      features, but it will make more sense for
                                                      the purpose of this analysis if those are
                                                      information-rich features.
        Projection_class.feature_names -- Type: list
                                          The colnames of the input matrix for Projection class.
                                          Also the colnames of the Projection_class.spec_cleaned_data
        Projection_class.sample_id -- Type: list
                                      The row names of the input matrix for Projection class.
                                      Also the row names of the Projection_class.spec_cleaned_data
    Attributes:
        spec_cleaned_df -- Type: pandas.DataFrame
        group_set -- Type: list
                     File names
        group_no_dict -- Type: dictionary
                         Key: self.group_set; value: group number (type: interger)
        differentiating_feature -- Type: list
    """

    def __init__(self, Projection_class):  # at cluster levels
        self.spec_cleaned_df = pandas.DataFrame(data = Projection_class.spec_cleaned_data,
                                                index = Projection_class.sample_id,
                                                columns = Projection_class.feature_names)
        self.spec_cleaned_df['group'] = tuple([element.split("__")[0] for element in Projection_class.sample_id])
        self.group_set = list(set(self.spec_cleaned_df['group']))

    def atGroup(self):
        group_set_num = len(self.group_set)
        group_no = list(range(group_set_num))
        self.group_no_dict = dict(zip(self.group_set, group_no))
        self.spec_cleaned_df['group_no'] = self.spec_cleaned_df['group'].map(self.group_no_dict)

        group_info = self.spec_cleaned_df[['group', 'group_no']]
        data_only = self.spec_cleaned_df.drop(columns = ['group', 'group_no'])

        pval_df = linearRegressionPVal(group_info['group_no'], data_only, silence_intersect = True)

        sign_pval_df = pval_df[(pval_df['pval'] < 0.1) & (pval_df['pval'] > 0.05)]
        sign_df = pandas.DataFrame(data = [1] * len(sign_pval_df.index),
                                   index = sign_pval_df.index,
                                   columns = ['sign_level'])

        high_sign_pval_df = pval_df[pval_df['pval'] < 0.05]
        high_sign_df = pandas.DataFrame(data = [2] * len(high_sign_pval_df.index),
                                        index = high_sign_pval_df.index,
                                        columns = ['sign_level'])

        merged_sign_df = pandas.concat([high_sign_df, sign_df], axis = 0, sort = True)

        self.differentiating_feature = list(merged_sign_df.index)
        self.differentiating_feature_df = merged_sign_df


def identifiedFeatures(args, current_wd, retrospect_dir, output_file_tag, suppress):
        ## take-in args
        bifurication_args = BifuricationArgs(args = args, current_wd = current_wd, suppress = suppress)

        for f in range(len(bifurication_args.input_files)):
            input_matrix = RawDataImport(file_name = bifurication_args.input_files[f], for_merging_file = True, suppress = False, second_chance = False)
            input_matrix.readCSV()

            info_rich = [value for value in input_matrix.data.columns.values if value in bifurication_args.list_of_info_rich]
            input_data = input_matrix.data[info_rich]

            if f == 0:
                merged_dataframe = input_data
            else:
                merged_dataframe = pandas.concat([merged_dataframe, input_data], axis = 0, sort = True)

        merged_dataframe = merged_dataframe.fillna(0)

        ## find feature(s) that responsible for differentiating groups in PCA space
        projection = Projection(merged_dataframe = merged_dataframe, normalize = bifurication_args.normalize)
        projection.cleanSpec()

        differentiating_features = DifferentiatingFeatures(projection)
        differentiating_features.atGroup()

        if output_file_tag != '':
            tag = [output_file_tag]
        else:
            tag = ['sign_level']

        output_file_name = os.path.join(retrospect_dir, (output_file_tag + '_differentiating_feature.csv'))

        differentiating_features.differentiating_feature_df.columns = tag

        print('Features that drive the separation among groups on PC space are:')
        print('(level 2: p value < 0.05; level 1: 0.05 < p value < 0.1)')
        print(differentiating_features.differentiating_feature_df)

        print('Output file:')
        print(output_file_name)
        differentiating_features.differentiating_feature_df.to_csv(output_file_name)

        # TODO: export raw_p_val

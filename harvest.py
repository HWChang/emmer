#!/usr/bin/env python3

# Usage:
# move to one level above emmer/
# python3 -m emmer.harvest -i emmer/data/data_dir_3 -f 'HardFilter' -u 2 -l 2 -t 2 -d 0.001 -z 0.33 -r

from .main.basic.math import NonDesityMatrix
from .main.basic.read import GetFiles, RawDataImport
#from .main.advanced.iteration import MinusOneVNE, MinDataLostFilter, InfoRichCalling, reproducibility, reproducibility_summary, Kernal
from .main.advanced.iteration import MinusOneVNE, InfoRichCalling, reproducibility, reproducibility_summary, Kernal
from .posthoc.visual.viewer import Projection, Plot
from .troubleshoot.warn.warning import *
from .troubleshoot.err.error import *
from .toolbox.recorder import initNoteBook, UpdateNoteBook
from .toolbox.technical import emptyNumpyArray

from scipy.spatial import procrustes
import itertools
import argparse
import pandas
import numpy
import math
import time
import glob
import sys
import os

start_time = time.time()
__version__ = '1.0'

"""
Take user-defined args and run emmer
"""

##==1==## define function and class
def tutorial():
    """
    ##==1==## Expected Data Format
    1. Expected csv file(s). When input multiple csv files as input, those csv files
       needed to be stored under the same folder. That folder should only contains your
       input csv file(s).
    2. Expect to have row names and column header. Examplary input file can be found
       under 'emmer/data/data_dir_3/'
       row names: sample names
       column headers: feature names
       elements: numeric values with on missing value
                 (Current version of emmer does not support input matrix with missing
                 values. In future update, the missing value will be converted to 0)
    3. Do not include '__' in your file name or row names

    ##==2==## Output Files and Format
    1. output/*_reproducibility.csv
       Store informaiton-rich feature calling reproducibilty. Emmer will not generate
       this file when running under QuickLook mode,
    2. output/information_rich_features_summary.csv
       Generate a summary when emmer working on multiple input files.
    3. output/*_colmean.csv
       Store means for each feature. Necessary for projecting new observation onto
       the existing PCA space.
    4. output/*_transformation_matrix.csv
       Store left signular matrix. Necessary for projecting new observation onto
       the existing PCA space.
    5. output/*_coordinates.csv or *_projection.csv
       Coordinates on the PCA space
    6. *_PCA_*.pdf
       PCA plot
    [!] The name and number of output files might varys depend on user's settings. Please
        refer to the Arugments setions for detail information about settings

    ##==3==## Quick Examples
    1. Input matrix contains counts, but you wish to converted the counts into fractional
       abundance before conducting your analysis.
       python3 -m emmer.harvest -i emmer/data/data_dir_3 -f 'HardFilter' -u 2 -l 2 -t 2 -d 0.001 -z 0.33 -r

    2. If you input data contains categorical values and want to conduct PCA by eigendecomposition
       of a correlation matrix.
       (Current version of emmer does not support this function. Will included in future update)

    ##==4==## Suggested Analytical Flow
    [Time is of the essence]
    1. A quick look
       python3 -m emmer.harvest -i emmer/data/data_dir_3 -f 'HardFilter' -u 2 -l 2 -d 0.001 -z 0.33 -r -p -q

    [Just what to be thorough]
    2. Report the reproducibilty of information-rich feature calling
       python3 -m emmer.harvest -i emmer/data/data_dir_3 -f 'HardFilter' -u 2 -l 2 -t 2 -d 0.001 -z 0.33 -r
    3. Fine tuning your thresholds
       python3 -m emmer.bake -m 'RevisitThreshold' -u 2.5,1.5,0.25 -l 2.5,1.5,0.25 -t 2,2,0 -e output/detail_vNE/ -i output/filtered_data/
    4. Redo analysis with the suggested information-rich feature calling thresholds

    [Picture paints a thousand words/Significant p value made my day]
    5. Export emmer.bake for additional options for generating plots and conducting statistical tests
       python3 -m emmer.bake -g

    ##==5==## Arugments
    Required:
    -i I               Input directory that contains one or many csv files or a path to specific csv file.
    -f F, -filter      Filter data before nominating information-rich features.
                       1. HardFilter: Remove column that contains -z levels of zeros. Require to set arugment -z.
                       2. None: No filer. Might take longer time to nominate information-rich feature.
    -u U               Upper limit when choosing information-rich feature. Default: 1. When set as 1, the
                       upper limitation is 1 standard deviation from the mean of the von Neumann entropies
                       of all remove-one-column matrices.
    -l L               Lower limit when choosing information-rich feature. Default: 1. When set as 1, the
                       lower limitation is 1 standard deviation from the mean of the von Neumann entropies
                       of all remove-one-column matrices.
    -t T               How many times a feature need to be nominate as information-rich feature in jackknife
                       subsampling to be included in the final list of information-rich features.

    Conditionally requried:
    -z, Z, zeroToleranceLevel
                       Must be a less than 1 but greater than 0. The number represents the maximum
                       fraction of element in each column of your input matrix that can be zero. Column that
                       exceeds this threshold will be remove before information-rich feature calling.

    Optional:
    -d D, -detectionLimit
                       Set the detection limit of our method. Must be numeric. Set number in the input
                       matrix that below this detection limit as zero before filtering. When using with -z,
                       emmer will conduct this step before running -z.
    -q Q, -quickLook   Default: False. If True, activate QuickLook mode. In QuickLook mode, emmer will not
                       calculate the reproducibility of information-rich feature calling. Default: False.
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -q
    -o O               Expect a string. This string will be tag to all your output file name from the analysis.
    -r R               Choose this option when you want emmer to convert your input data into fractional abundance.
                       Default: False.
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -r
    -n N, normalize    Choose this option when your features (columns) are measured in different units. When set as True,
                       EMMER will normalize each column the input data by its standard deviation.
                       Default: False.
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -n
    -p P, plot         Visualize emmer result with PCA plot(s). Default: False.
                       (Currently emmer cannot generate PCA plot if it only works on input file. Also,
                       user might experience error when generateing 2D PCA plots. These issue will be
                       addressed in future updates)
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -p
                       [!] An interactive plot that allows user to adjust angles. Save the plot as pdf
                           after user close the window.
    -s S, sanityCheck  Generate three or six PCA plots (and their corresponding output csv files) depend on
                       the filter of choose. Default: False.
                       1: Full dataset
                       2: filtered-out data (if filter is not set at 'None')
                       3: filtered data (if filter is not set at 'None')
                       4: filtered, non-information-rich data (if filter is not set at 'None')
                          non-information-rich data (if filter is set at 'None')
                       5: Information-rich data
                       6. filtered-out data combined with filtered, non-information-rich data
                          (if filter is not set at 'None')
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -s
    -c C, -cpuNum      Support multiprocessing. This argument is used to set the number of CPU used in the analysis.
    -w W, -writeDownDetails
                       Do you want to add additional notes as emmer run? Default: False.
                       (Not available,. Will be included in future update)
                       Usage:
                       python3 -m emmer.harvest <other_arguments_and_inputs> -w
    """
    pass


class HarvestArgs:
    """
    Take arguments and report error messages when necessary

    Objective: so we can test and use @

    Argument:
        suppress -- Type: boolean
                    Should emmer end program after error arise. Set at False when
                    running unittest
        silence -- Type: boolean
                   When set as True. Silence warning messages
        neglect -- Type: boolean
                   Suppress notebook initation when running unittest

    Attributes:
        suppress -- Type: boolean
        silence -- Type: boolean
        neglect -- Type: boolean
        notebook_name -- Type: str
                         Notebook file name with full path
        args -- Type: argparse.Namespace
                Store the user input parameters from command line
        input_dir -- Type: str
                     Corresponding to args.i
        input -- Type: emmer.main.basic.read.GetFiles
        specific_csv -- Type: boolean
                        Set True if <self.input_dir> is a specific csv file. False when <self.input_dir>
                        is a directory
        quick_look -- Type: boolean
                      Corresponding to args.q
        infoRich_threshold -- Type: int
                              Corresponding to args.t
        output_file_tag -- Type: str
                           Corresponding to args.o
        use_fractional_abundance -- Type: boolean
                                    Corresponding to args.r
        detection_limit -- Type: float
                           Corresponding to args.d
        filter -- Type: str
                  Corresponding to args.f
        upper_threshold_factor -- Type: float or str ('None')
                                  Corrresponding to args.u
        lower_threshold_factor -- Type: float or str ('None')
                                  Corrresponding to args.l
        plot_result -- Type: float
                       Corresponding to args.p
        sanity_check_plots -- Type: boolean
                              Corresponding to args.s
        warning_code -- Type: str
                        For unittest
        normalize -- Type: boolean
                     Scale each column in the mean centered data based on its standard deviation
                     before SVD
    """
    def __init__(self, suppress, silence, neglect):
        parser = argparse.ArgumentParser(description = '#############################################################################\nPlease use -g when you need additional explanation on different modes their corresponding arguments. Try: python3 -m emmer.harvest -g\n#############################################################################')
        parser.add_argument('-g', '-guide', action = 'store_true')
        parser.add_argument('-i', type = str)
        parser.add_argument('-q', '-quickLook', action = 'store_true')
        parser.add_argument('-o', type = str)
        parser.add_argument('-r', action = 'store_true')
        parser.add_argument('-n', '-normalize', action = 'store_true')
        parser.add_argument('-d', '-detectionLimit', type = float)
#        parser.add_argument('-f', '-filter', type = str, choices = ['MinDataLostFilter', 'HardFilter', 'None'])
        parser.add_argument('-f', '-filter', type = str, choices = ['HardFilter', 'None'])
        parser.add_argument('-z', '-zeroToleranceLevel', type = float)
        parser.add_argument('-t', type = int)
        parser.add_argument('-u', type = float)
        parser.add_argument('-l', type = float)
        parser.add_argument('-p', '-plot', action = 'store_true')
        parser.add_argument('-s', '-sanityCheck', action = 'store_true')
        parser.add_argument('-c', '-cpuNum', default = 1, type = int)
        parser.add_argument('-w', '-writeDownDetails', action = 'store_true')
        self.args = parser.parse_args()
        self.suppress = suppress
        self.neglect = neglect
        self.silence = silence

        if self.args.g:
            print(tutorial.__doc__)
            sys.exit()


    def getArgsO(self):
        if self.args.o:
            self.output_file_tag = self.args.o
        else:
            self.output_file_tag = ''


    def getArgsW(self):
        self.notebook_name = initNoteBook(current_wd = os.getcwd(), script_name = 'emmer.harvest', script_version = __version__, tag = self.output_file_tag,
                                          neglect = self.neglect, explicit = self.args.w)


    def getArgsI(self):
        self.input_dir = self.args.i
        self.specific_csv = False
        try:
            if os.path.isdir(self.input_dir) == True:
                self.input = GetFiles(self.input_dir)
            elif self.input_dir.endswith('.csv') == True:
                self.specific_csv = True
            elif os.path.isdir(self.input_dir) == False and self.input_dir.endswith('.csv') == False:
                raise Error(code = '1')

        except Error as e:
            raise ErrorCode1(suppress = self.suppress) from e


    def getArgsQT(self):
        if self.args.q:
            self.quick_look = True
            self.infoRich_threshold = 1

            try:
                if self.args.t:
                    raise WarningCode10(silence = self.silence)
            except WarningCode10:
                self.warning_code = '10'
                self.infoRich_threshold = 1


        else:
            self.quick_look = False

            if self.args.t:
                self.infoRich_threshold = self.args.t
            else:
                self.infoRich_threshold = 2


    def getArgsR(self):
        if self.args.r:
            self.use_fractional_abundance = True
        else:
            self.use_fractional_abundance = False


    def getArgsN(self):
        if self.args.n:
            self.normalize = True
        else:
            self.normalize = False


    def getArgsD(self):
        if self.args.d:
            self.detection_limit = self.args.d
        else:
            self.detection_limit = 0


    def getArgsFZ(self):
        if self.args.f == 'HardFilter':
            self.filter = self.args.f

            # missing args.z
            try:
                if not self.args.z:
                    raise Error(code = '3')
            except Error as e:
                raise ErrorCode3(suppress = self.suppress) from e

            # incorrect args.z number setting
            try:
                if self.args.z > 0 and self.args.z <= 1:
                    self.tolerance = self.args.z
                else:
                    raise Error(code = '2')
            except Error as e:
                raise ErrorCode2(suppress = self.suppress) from e

            if self.args.d:
                self.detection_limit = self.args.d

        else:
            self.tolerance = 1
            self.filter = 'None'

            try:
                if self.args.z:
                    raise WarningCode2(silence = self.silence)
            except:
                self.warning_code = '2'


    def getArgsUL(self):
        try:
            if self.args.u and self.args.l:
                self.upper_threshold_factor = self.args.u
                self.lower_threshold_factor = self.args.l
            elif self.args.u:
                self.upper_threshold_factor = self.args.u
                self.lower_threshold_factor = 'None'
            elif self.args.l:
                self.lower_threshold_factor = self.args.l
                self.upper_threshold_factor = 'None'
            else:
                raise Error(code = '5')
        except Error as e:
            raise ErrorCode5(suppress = self.suppress) from e


    def getArgsPS(self):
        if self.args.p:
            self.plot_result = True

            if self.args.s:
                self.sanity_check_plots = True
            else:
                self.sanity_check_plots = False

        else:
            self.plot_result = False

            if self.args.s:
                self.sanity_check_plots = True
            else:
                self.sanity_check_plots = False

        # prevent user setting errors
        if self.args.s:
            try:
                if self.specific_csv == True or len(self.input.input_files) == 1:
                    raise WarningCode3(silence = self.silence)
            except:
                self.warning_code = '3'

        if self.args.p:
            try:
                if self.specific_csv == True or len(self.input.input_files) == 1:
                    raise WarningCode5(silence = self.silence)
            except:
                self.warning_code = '5'


    def getArgsC(self):
        try:
            if os.cpu_count() < self.args.c or self.args.c == 0:
                raise Error(code = '47')
            else:
                self.num_cpu = self.args.c
        except Error as e:
            raise ErrorCode47(suppress = self.suppress) from e


    def processArgs(self):
        self.getArgsO()
        self.getArgsW()
        self.getArgsI()
        self.getArgsQT()
        self.getArgsR()
        self.getArgsN()
        self.getArgsD()
        self.getArgsFZ()
        self.getArgsUL()
        self.getArgsPS()
        self.getArgsC()
        UpdateNoteBook(notebook_name = self.notebook_name, neglect = self.neglect).updateArgs(args = self.args)


class EMMER:
    """
    Take in user-defined parameters and input file(s) and identify list(s) of information-rich
    features. When ask to process multiple files, those files need to be store in the same directory.
    Also, all those files will subject to the same processing parameters.
    """

    def __init__(self, input_dir, output_file_tag, detection_limit, tolerance,
                 filter, upper_threshold_factor, lower_threshold_factor, specific_csv,
                 infoRich_threshold, num_cpu, notebook_name, neglect, quick_look,
                 use_fractional_abundance, normalize):

        self.output_file_tag = str(output_file_tag)
        self.detection_limit = detection_limit
        self.tolerance = tolerance
        self.filter = filter
        self.upper_threshold_factor = upper_threshold_factor
        self.lower_threshold_factor = lower_threshold_factor
        self.num_cpu = num_cpu
        self.infoRich_threshold = infoRich_threshold
        self.notebook_name = notebook_name
        self.neglect = neglect
        self.quick_look = quick_look
        self.use_fractional_abundance = use_fractional_abundance
        self.normalize = normalize
        self.collections_of_info_rich_features = []

        ## import all csv file store under input_dir
        if specific_csv == True:
            self.input_file_names = [input_dir]
        else:
            self.input_file_names = GetFiles(input_dir).input_files

        self.current_wd = os.getcwd()
        self.output_dir = os.path.join(self.current_wd, 'output')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.ra_data_output_dir = os.path.join(self.output_dir, 'pre_filter_data')
        if not os.path.exists(self.ra_data_output_dir):
            os.makedirs(self.ra_data_output_dir)

        self.filter_out_data_output_dir = os.path.join(self.output_dir, 'filtered_out_data')
        if not os.path.exists(self.filter_out_data_output_dir):
            os.makedirs(self.filter_out_data_output_dir)

        self.filter_data_output_dir = os.path.join(self.output_dir, 'filtered_data')
        if not os.path.exists(self.filter_data_output_dir):
            os.makedirs(self.filter_data_output_dir)

        self.raw_not_infoRich_data_output_dir = os.path.join(self.output_dir, 'raw_not_infoRich_data')
        if not os.path.exists(self.raw_not_infoRich_data_output_dir):
            os.makedirs(self.raw_not_infoRich_data_output_dir)

        self.detail_vNE = os.path.join(self.output_dir, 'detail_vNE')
        if not os.path.exists(self.detail_vNE):
            os.makedirs(self.detail_vNE)


    def singleFile(self, current_file_no = 0, silence = False):
        self.input_basename = os.path.basename(self.input_file_names[current_file_no])
        self.silence = silence
        self.data = Kernal(file_name = self.input_file_names[current_file_no], detection_limit = self.detection_limit,
                           tolerance = self.tolerance, filter = self.filter, upper_lim = self.upper_threshold_factor,
                           lower_lim = self.lower_threshold_factor, infoRich_threshold = self.infoRich_threshold,
                           quick_look = self.quick_look, use_fractional_abundance = self.use_fractional_abundance,
                           vNE_output_folder =  self.detail_vNE, output_file_tag = self.output_file_tag, num_cpu = self.num_cpu,
                           notebook_name = self.notebook_name, normalize = self.normalize, neglect = self.neglect,
                           silence = self.silence)

        self.data.importAndProcess()

        ## modify index value of filtered dataset
        index_tag = self.input_basename.replace(".csv", "__")
        clean_df = self.data.filtered_data.data
        clean_df.index = [index_tag + element for element in self.data.filtered_data.sample_id]

        ## prepare file names
        pre_filter_data_file_name = os.path.join(self.ra_data_output_dir, self.input_basename.replace(".csv", "")) + self.output_file_tag + "__pre_filterd_data.csv"
        filter_out_data_file_name = os.path.join(self.filter_out_data_output_dir, self.input_basename.replace(".csv", "")) + self.output_file_tag + "__filterd_out_data.csv"
        clean_df_file_name = os.path.join(self.filter_data_output_dir, self.input_basename.replace(".csv", "")) + self.output_file_tag + "__filterd_data.csv"
        raw_not_infoRich_data_name = os.path.join(self.raw_not_infoRich_data_output_dir, self.input_basename.replace(".csv", "")) + self.output_file_tag + "__raw_not_infoRich_data.csv"

        if current_file_no == 0:
            self.pre_filter_data_file_names = [pre_filter_data_file_name]
            self.filter_out_data_file_names = [filter_out_data_file_name]
            self.clean_df_file_names = [clean_df_file_name]
            self.raw_not_infoRich_data_name = [raw_not_infoRich_data_name]

        else:
            self.pre_filter_data_file_names.append(pre_filter_data_file_name)
            self.filter_out_data_file_names.append(filter_out_data_file_name)
            self.clean_df_file_names.append(clean_df_file_name)
            self.raw_not_infoRich_data_name.append(raw_not_infoRich_data_name)

        clean_df.to_csv(clean_df_file_name)

        ## get prefilter data
        #   raw_data -> relativeAbundance()
        self.data.input_matrix.data.index = index_tag + self.data.input_matrix.data.index
        self.data.input_matrix.raw_data_before_filter.index = [index_tag + element for element in self.data.input_matrix.sample_id]
        self.data.input_matrix.raw_data_before_filter.to_csv(pre_filter_data_file_name)

        ## get and export filtered out dataset
        #   raw_data -> relativeAbundance(); .raw_data_before_filter !-> pass filter
        features_that_fail_at_filtering = [value for value in self.data.input_matrix.raw_data_before_filter.columns if value not in list(clean_df.columns)]
        fail_filter = self.data.input_matrix.raw_data_before_filter[features_that_fail_at_filtering]
        fail_filter.to_csv(filter_out_data_file_name)

        ## Identify information-rich features
        self.data.infoRichCallingAndReproducibility()

        if self.quick_look == False:
            self.output_file_name = os.path.join(self.output_dir, self.input_basename.replace(".csv", "")) + self.output_file_tag + "_reproducibility.csv"
            self.data.info_rich_features_w_reproducibility.to_csv(self.output_file_name)

        ## get filter_out_and_no_information-rich
        #   raw_data -> remove infoRich features
        not_infoRich_features_in_raw_data = [value for value in self.data.input_matrix.raw_data_before_filter.columns if value not in self.data.list_of_info_rich_features]
        filter_out_and_not_infoRich_data_file_name = self.data.input_matrix.raw_data_before_filter[not_infoRich_features_in_raw_data]
        filter_out_and_not_infoRich_data_file_name.to_csv(raw_not_infoRich_data_name)

        ## collect the names of information-rich features
        self.collections_of_info_rich_features.append(self.data.list_of_info_rich_features)


    def multipleFiles(self):
        ## identify information-rich feature for individaul file
        for i in range(len(self.input_file_names)):
            self.singleFile(i)

            file_name_sub = [str(self.input_basename)]
            if self.quick_look == True:
                info_rich_feature_sub = self.data.list_of_info_rich_features
                reproducibility_sub = [1] * len(info_rich_feature_sub)

            else:
                info_rich_feature_sub = self.data.list_of_info_rich_features
                reproducibility_sub = list(self.data.info_rich_features_w_reproducibility['repreducibility (%)'])

            reproducibility_sub = numpy.round(numpy.array(reproducibility_sub), decimals = 2)
            summary_df_sub = pandas.DataFrame(reproducibility_sub, columns = file_name_sub, index = info_rich_feature_sub)

            if i == 0:
                self.summary_df = summary_df_sub

            else:
                # similar to cbind() and keep all
                self.summary_df = pandas.concat([self.summary_df, summary_df_sub], axis = 1, sort = True)

        self.summary_df = self.summary_df.fillna(0)
        self.summary_df.to_csv(os.path.join(self.output_dir, "information_rich_features_summary.csv"))
        self.list_of_info_rich_features_found_in_files = list(self.summary_df.index)

        ## keep unique information-rich feature names
        self.collections_of_info_rich_features = list(set(list(itertools.chain(*self.collections_of_info_rich_features))))


def mergeDataFrame(EMMER_class, select, file_name_list, info_rich_list, notebook_name, normalize, neglect):
    """
    Allow user to merge different kinds of csv files:

    select:
    'pre_filter': prefilter csv files
    'filtered_excluded': data the fail to pass filter
    'filtered': filtered data before informaiton-rich feature calling
    'filtered_infoRich': filtered data that contains only information-rich features
    'filtered_no_infoRich': filtered data without information-rich features
    'raw_not_infoRich': raw data without information-rich features
    """

    print(f"Merging data frame with {select} as column selection condition...")

    combine_list_of_informoation_rich_features = list(EMMER_class.summary_df.index.values)

    for i in range(len(file_name_list)):
        input_basename = os.path.basename(file_name_list[i])

        input_matrix = RawDataImport(file_name = file_name_list[i], for_merging_file = True, suppress = False, second_chance = False)
        input_matrix.readCSV()

        dataframe_for_merging = pandas.DataFrame(input_matrix.data,
                                                 columns = input_matrix.feature_names,
                                                 index = input_matrix.sample_id)

        ## Need to select specific columns
        # 'filtered_infoRich', 'filtered_no_infoRich'
        #
        #  Select only the columns that were nominated as combine_list_of_informoation_rich_features
        #  Not all of the feature in self.dataframe_for_merging can be found in combine_list_of_informoation_rich_features
        #  To avoid error msg, first take the intersect between the two lists, then subset the data
        if select == 'filtered_no_infoRich':
            targeted_features_in_this_dataset = [value for value in dataframe_for_merging.columns.values if value not in combine_list_of_informoation_rich_features]
            select_data_for_merging = dataframe_for_merging[targeted_features_in_this_dataset]
        elif select == 'filtered_infoRich':
            targeted_features_in_this_dataset = [value for value in dataframe_for_merging.columns.values if value in combine_list_of_informoation_rich_features]
            select_data_for_merging = dataframe_for_merging[targeted_features_in_this_dataset]

        ## Don't need to select specific columns
        # 'pre_filter', 'filtered_excluded', 'filterd'
        else:
            select_data_for_merging = dataframe_for_merging

        ## Merging dataframes
        if i == 0:
            merged_dataframe = select_data_for_merging
        else:
            # similar to rbind() and keep all
            merged_dataframe = pandas.concat([merged_dataframe, select_data_for_merging], axis = 0, sort = True)

    # remove infoRich feature in raw_not_infoRich inputs
    # why it happens: feature_1 is not an information-rich feature in file_1 but is in file_2.
    #                 Merging raw_not_infoRich_file_1 and raw_not_infoRich_file_2 will include
    #                 feature_1. We need to remove it.
    if select == 'raw_not_infoRich':
        intersect_feature_name = list(set(info_rich_list).intersection(merged_dataframe.columns.values))
        merged_dataframe.drop(intersect_feature_name, axis = 1, inplace = True)

    EMMER_class.merged_dataframe = merged_dataframe.fillna(0)

    transform_info = Projection(merged_dataframe = EMMER_class.merged_dataframe, normalize = normalize)

    transform_info.V_df.to_csv(os.path.join(EMMER_class.output_dir, (select + "__transformation_matrix.csv")))
    transform_info.colmean_df.to_csv(os.path.join(EMMER_class.output_dir, (select + "__data_colmean.csv")))

    if normalize == True:
        transform_info.colstd_df.to_csv(os.path.join(EMMER_class.output_dir, (select + "__data_colstd.csv")))

    transform_info.projection_df.to_csv(os.path.join(EMMER_class.output_dir, (select + "__PCA_coordinates.csv")))
    transform_info.PC_annotation.to_csv(os.path.join(EMMER_class.output_dir, (select + "__percent_explained.csv")))

    notebook = UpdateNoteBook(notebook_name = notebook_name, neglect = neglect)
    notebook.updateMergeResult(merge_what = select, num_feature = merged_dataframe.shape[1], norm_eigen = transform_info.norm_eigvals)

    return(transform_info)


def sanityCheck(EMMER_class, input_file_names, current_filter, notebook_name, neglect, normalize, make_plot = False):
    """
    For generate datasets and plots for santiy check
    """
    if current_filter != 'None':
        Projection_class_in_list = [mergeDataFrame(EMMER_class = EMMER_class, select = 'pre_filter', file_name_list = emmer_result.pre_filter_data_file_names, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered_excluded', file_name_list = emmer_result.filter_out_data_file_names, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered', file_name_list = emmer_result.clean_df_file_names, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered_no_infoRich', file_name_list = emmer_result.clean_df_file_names, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered_infoRich', file_name_list = emmer_result.clean_df_file_names, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'raw_not_infoRich', file_name_list = emmer_result.raw_not_infoRich_data_name, normalize = normalize,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect)]
        input_file_in_list_of_list = [input_file_names]
        output_file_name_in_list = [(EMMER_class.output_file_tag + '__pre_filter_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_excluded_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_no_infoRich_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_infoRich_projection.csv'),
                                    (EMMER_class.output_file_tag + '__raw_not_infoRich_projection.csv')]
        index_tag_list = ['__pre_filter_projection.csv', '__filtered_excluded_projection.csv', '__filtered_projection.csv',
                          '__filtered_no_infoRich_projection.csv', '__filtered_infoRich_projection.csv', '__raw_not_infoRich_projection.csv']
        dataset_list = ['pre_filter', 'filtered_excluded', 'filtered', 'filtered_no_infoRich', 'filtered_infoRich', 'raw_not_infoRich']

        for p in range(6):
            Projection_class_in_list[p].projection_df.to_csv(output_file_name_in_list[p])

            if 'PC3' not in Projection_class_in_list[p].projection_df:   # TODO: should work, but need testing
                new_projection_df = Projection_class_in_list[p].projection_df.iloc[:, 0:2]
                original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:2])
                new_projection = numpy.array(new_projection_df)
            else:
                new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
                original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:3])

            notebook = UpdateNoteBook(notebook_name = notebook_name, neglect = neglect)

            if new_projection.size != 0:
                mtx1, mtx2, disparity = procrustes(original_projection, new_projection)
                notebook.updateProcrustesResult(procrustes_score = disparity, which_dataset = dataset_list[p], no_procrustes_score = False)
            else:
                notebook.updateProcrustesResult(procrustes_score = '', which_dataset = '', no_procrustes_score = True)


#        original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:3])
#
#        for p in range(6):
#            Projection_class_in_list[p].projection_df.to_csv(output_file_name_in_list[p])
#
#            new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
#            #if 'PC3' not in Projection_class_in_list[p].projection_df: TODO:
#            #    new_projection_df = Projection_class_in_list[p].projection_df.iloc[:, 0:2]
#            #    r, c = new_projection_df.shape
#            #    new_projection_df.iloc[3] = [0] * r
#            #    new_projection = numpy.array(new_projection_df)
#            #else:
#            #    new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
#            notebook = UpdateNoteBook(notebook_name = notebook_name, neglect = neglect)
#            if new_projection.size != 0:
#                mtx1, mtx2, disparity = procrustes(original_projection, new_projection)
#                notebook.updateProcrustesResult(procrustes_score = disparity, which_dataset = dataset_list[p], no_procrustes_score = False)
#            else:
#                notebook.updateProcrustesResult(procrustes_score = '', which_dataset = '', no_procrustes_score = True)


    else:
        Projection_class_in_list = [mergeDataFrame(EMMER_class = EMMER_class, select = 'pre_filter', file_name_list = emmer_result.pre_filter_data_file_names,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered_no_infoRich', file_name_list = emmer_result.clean_df_file_names,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect),
                                    mergeDataFrame(EMMER_class = EMMER_class, select = 'filtered_infoRich', file_name_list = emmer_result.clean_df_file_names,
                                                   info_rich_list = emmer_result.collections_of_info_rich_features, notebook_name = notebook_name, neglect = neglect)]
        input_file_in_list_of_list = [input_file_names]
        output_file_name_in_list = [(EMMER_class.output_file_tag + '__pre_filter_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_no_infoRich_projection.csv'),
                                    (EMMER_class.output_file_tag + '__filtered_infoRich_projection.csv')]
        index_tag_list = ['__pre_filter_projection.csv', '__filtered_no_infoRich_projection.csv', '__filtered_infoRich_projection.csv']
        dataset_list = ['pre_filter', 'filtered_no_infoRich', 'filtered_infoRich']
#        original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:3])
#
#        for p in range(3):
#            Projection_class_in_list[p].projection_df.to_csv(output_file_name_in_list[p])
#            new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
#
#            # FIXME
#            #if 'PC3' not in Projection_class_in_list[p].projection_df:
#            #    new_projection_df = Projection_class_in_list[p].projection_df.iloc[:, 0:2]
#            #    r, c = new_projection_df.shape
#            #    new_projection_df.iloc[3] = [0] * r
#            #    new_projection = numpy.array(new_projection_df)
#            #else:
#            #    new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
#            notebook = UpdateNoteBook(notebook_name = notebook_name, neglect = neglect)
#            if new_projection.size != 0:
#                mtx1, mtx2, disparity = procrustes(original_projection, new_projection)
#                notebook.updateProcrustesResult(procrustes_score = disparity, which_dataset = dataset_list[p], no_procrustes_score = False)
#            else:
#                notebook.updateProcrustesResult(procrustes_score = '', which_dataset = '', no_procrustes_score = True)


        # works, but need unittest
        for p in range(3):
            Projection_class_in_list[p].projection_df.to_csv(output_file_name_in_list[p])

            if 'PC3' not in Projection_class_in_list[p].projection_df:
                new_projection_df = Projection_class_in_list[p].projection_df.iloc[:, 0:2]
                original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:2])
                new_projection = numpy.array(new_projection_df)
            else:
                new_projection = numpy.array(Projection_class_in_list[p].projection_df.iloc[:, 0:3])
                original_projection = numpy.array(Projection_class_in_list[0].projection_df.iloc[:, 0:3])

            notebook = UpdateNoteBook(notebook_name = notebook_name, neglect = neglect)

            if new_projection.size != 0:
                mtx1, mtx2, disparity = procrustes(original_projection, new_projection)
                notebook.updateProcrustesResult(procrustes_score = disparity, which_dataset = dataset_list[p], no_procrustes_score = False)
            else:
                notebook.updateProcrustesResult(procrustes_score = '', which_dataset = '', no_procrustes_score = True)


    if make_plot == True:
        output_file_name_in_list = EMMER_class.output_dir + EMMER_class.output_file_tag + '__sanity_check_PCAs.pdf'
        sanity_check_plots = Plot(Projection_class_in_list, input_file_in_list_of_list, output_file_name_in_list, current_filter)
        sanity_check_plots.viewSanityCheckPlots()


##==2==## running emmer.harvest
if __name__ == '__main__':
    processed_args = HarvestArgs(suppress = False, silence = False, neglect = False)
    processed_args.processArgs()

    emmer_result = EMMER(input_dir = processed_args.input_dir, output_file_tag = processed_args.output_file_tag,
                         detection_limit = processed_args.detection_limit, tolerance = processed_args.tolerance,
                         filter = processed_args.filter, upper_threshold_factor = processed_args.upper_threshold_factor,
                         lower_threshold_factor = processed_args.lower_threshold_factor, num_cpu = processed_args.num_cpu,
                         specific_csv = processed_args.specific_csv, infoRich_threshold = processed_args.infoRich_threshold,
                         notebook_name = processed_args.notebook_name, neglect =  processed_args.neglect,
                         quick_look = processed_args.quick_look, normalize = processed_args.normalize,
                         use_fractional_abundance = processed_args.use_fractional_abundance)

    if processed_args.specific_csv == True:
        emmer_result.singleFile()
    else:
        if len(processed_args.input.input_files) > 1:
            emmer_result.multipleFiles()
            transform_info = mergeDataFrame(EMMER_class = emmer_result, select = 'filtered_infoRich',
                                            file_name_list = emmer_result.clean_df_file_names,
                                            info_rich_list = emmer_result.collections_of_info_rich_features,
                                            notebook_name = processed_args.notebook_name, normalize = processed_args.normalize,
                                            neglect =  processed_args.neglect)
        else:
            emmer_result.singleFile()

    print("computation time: %s seconds " % (time.time() - start_time))
    run_time = (time.time() - start_time)

    if processed_args.plot_result == True and processed_args.sanity_check_plots == False:
        processed_args.output_file_name = emmer_result.output_dir + emmer_result.output_file_tag + '__PCA_w_info_rich.pdf'
        visualizing_result = Plot(Projection_class_in_list = [transform_info],
                                  input_file_in_list_of_list = [processed_args.input.input_files],
                                  output_file_name = processed_args.output_file_name,
                                  filter = processed_args.filter)
        visualizing_result.viewSinglePCAplot()

    if processed_args.sanity_check_plots == True:
        os.chdir(emmer_result.output_dir)
        sanityCheck(EMMER_class = emmer_result, input_file_names = processed_args.input.input_files,
                    current_filter = processed_args.filter, make_plot = processed_args.plot_result,
                    notebook_name = processed_args.notebook_name, neglect =  processed_args.neglect,
                    normalize = processed_args.normalize)

    notebook = UpdateNoteBook(notebook_name = processed_args.notebook_name, neglect =  processed_args.neglect).updateRunTime(run_time = run_time)

    if processed_args.neglect == False:
        print('\nAnalytical parameters and brief summary stores at:\n' + processed_args.notebook_name)

    if os.cpu_count() > processed_args.args.c and processed_args.args.c == 1:
        print(f'\n[!] Tip: your computer has {os.cpu_count()} CPUs, but you only used one to run emmer.\n    Please consider to speed up your analysis by assign more than one CPU when running emmer with -c option.\n    Suggested number of CPU: {os.cpu_count() - 1}\n')

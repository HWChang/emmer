#!/usr/bin/env python3

## usage
# at a level above emmer/
# python3 -m emmer.test.test_iteration

import unittest
from ..main.basic.math import NonDesityMatrix
from ..main.basic.read import RawDataImport
from ..main.advanced.iteration import MinusOneVNE, InfoRichCalling, reproducibility, reproducibility_summary, Kernal
from ..troubleshoot.warn.warning import *
from ..troubleshoot.err.error import ErrorCode4, ErrorCode6
import numpy
import pandas
import sys
import os


class TestMinusOneVNE(unittest.TestCase):

    def test_minusOneVNE(self, col_to_remove = 1, num_cpu = 1):
        print('\ntest_MinusOneVNE.minusOneVNE:')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        InputA = MinusOneVNE(data = A, normalize = False, feature_names = ["col1", "col2", "col3", "col4"],  num_cpu = 1)
        my_result = InputA.minusOneVNE(col_to_remove = 1)
        #my_result[1] = numpy.round(my_result[1], decimals = 8)
        my_result[2] = numpy.round(my_result[2], decimals = 8)

        #expected_result = ['col2', 0.60207691]
        expected_result = [1, 'col2', 0.60207691]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_minusOneResult(self):
        print('\ntest_MinusOneVNE.minusOneResult:')
        A = numpy.array([[1, 4, 5, 12], [5, 8, 9, 0], [6, 7, 11, 19]])
        InputA = MinusOneVNE(data = A, normalize = False, feature_names = ["col1", "col2", "col3", "col4"], num_cpu = 1)
        InputA.minusOneResult()
        my_result = list(numpy.round(numpy.array(InputA.result_summary['vNE']), decimals = 6))

        expected_result = [0.529410, 0.602077, 0.478102, 0.268291]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


class TestInfoRichCalling(unittest.TestCase):

    def test_infoRichSelect(self):
        print('\ntest_InfoRichCalling.infoRichSelect:')
        print('        case 1: expect to work')
        file_name = 'emmer/data/test_case_1.csv'
        input_matrix = RawDataImport(file_name = file_name)
        input_matrix.readCSV()
        input_matrix.relativeAbundance()
        input_data = numpy.array(input_matrix.data)
        feature_names = list(input_matrix.feature_names)

        # filter == 'None'
        filtered_data = input_matrix

        info_rich_result = InfoRichCalling(data = filtered_data.data, current_feature_names = filtered_data.feature_names,
                                           upper_threshold_factor = 1, lower_threshold_factor = 1, normalize = False,
                                           num_cpu = 1, direct_from_result_summary = '')
        info_rich_result.infoRichSelect()
        my_result = list(info_rich_result.info_rich_feature['feature_name'])
        expected_result = ['col2', 'col3', 'col6']
        self.assertListEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('        case 2: raise error code 4')
        with self.assertRaises(ErrorCode4):
            file_name = 'emmer/data/test_case_1.csv'
            input_matrix = RawDataImport(file_name = file_name)
            input_matrix.readCSV()
            input_matrix.relativeAbundance()
            input_data = numpy.array(input_matrix.data)
            feature_names = list(input_matrix.feature_names)

            # filter == 'None'
            filtered_data = input_matrix

            info_rich_result = InfoRichCalling(data = filtered_data.data, current_feature_names = filtered_data.feature_names,
                                               upper_threshold_factor = 100, lower_threshold_factor = 100, normalize = False,
                                               num_cpu = 1, direct_from_result_summary = '', suppress = True)
            info_rich_result.infoRichSelect()
        print('===========================================================')


class Test_reproducibility_summary(unittest.TestCase):

    def test_reproducibility_summary(self):
        print('\ntest_reproducibility_summary:')
        file_name = 'emmer/data/test_case_1.csv'
        input_matrix = RawDataImport(file_name = file_name)
        input_matrix.readCSV()
        input_matrix.relativeAbundance()
        input_data = numpy.array(input_matrix.data)
        feature_names = list(input_matrix.feature_names)

        # filter == 'None'
        filtered_data = input_matrix

        infoRich_dict = {}
        info_rich_result = InfoRichCalling(data = filtered_data.data, current_feature_names = filtered_data.feature_names,
                                           upper_threshold_factor = 1, lower_threshold_factor = 1, num_cpu = 1,
                                           normalize = False, direct_from_result_summary = '')
        nrow = numpy.size(numpy.array(filtered_data.data), 0)

        info_rich_features_w_reproducibility = reproducibility_summary(filtered_matrix = filtered_data.data,
                                                                       infoRich_dict = reproducibility(InfoRichCalling_class = info_rich_result,
                                                                                                       infoRich_dict = infoRich_dict, nrow = nrow,
                                                                                                       basename = '', vNE_output_folder = '',
                                                                                                       output_file_tag = '', num_cpu = 1,
                                                                                                       normalize = False,
                                                                                                       direct_from_result_summary = ''))

        my_result = list(info_rich_features_w_reproducibility['occurrence'])
        expected_result = [4, 2, 3, 4, 1]
        self.assertListEqual(my_result, expected_result)

        my_result = list(info_rich_features_w_reproducibility['feature_name'])
        expected_result = ['col3', 'col5', 'col2', 'col6', 'col1']
        self.assertListEqual(my_result, expected_result)
        os.remove('__sub_0_detail_vNE.csv')
        os.remove('__sub_1_detail_vNE.csv')
        os.remove('__sub_2_detail_vNE.csv')
        os.remove('__sub_3_detail_vNE.csv')
        os.remove('__sub_4_detail_vNE.csv')
        os.remove('__sub_5_detail_vNE.csv')
        print('===========================================================')


class TestKernal(unittest.TestCase):

    def test_importAndProcess(self):
        ## use "HardFilter"
        print('        ---------------------------------------------------')
        print('        case 1: HardFilter (only set zero_tolerance)')
        print('             1.1: set detection limit correctly?')
        print('    file_names: test_case_3.csv')
        file_names = 'emmer/data/data_dir_1/test_case_1.csv'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 0.6')
        tolerance = 0.6
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_lim: 1')
        upper_lim = 1
        print('    lower_lim: 1')
        lower_lim = 1
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look_1: True')
        quick_look_1 = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_1, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)
        data.importAndProcess()

        my_result = data.detection_limit
        expected_result = 0
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             1.2: set filter correctly?')
        my_result = data.filter
        expected_result = 'HardFilter'
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             1.3: remove correct features')
        my_result = list(data.filtered_data.data.columns.values)
        expected_result = ['col1', 'col2', 'col3', 'col5', 'col6']
        self.assertListEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             1.4: error handling')
        print('                  unexpected detection limit setting')
        file_names = 'emmer/data/data_dir_1/test_case_1.csv'
        print('    detection_limit: 100')
        detection_limit = 100
        print('    tolerance: 0.6')
        tolerance = 0.6
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_lim: 1')
        upper_lim = 1
        print('    lower_lim: 1')
        lower_lim = 1
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look_1: True')
        quick_look_1 = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        with self.assertRaises(ErrorCode6):
            data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                          filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                          quick_look = quick_look_1, use_fractional_abundance = use_fractional_abundance,
                          vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                          num_cpu = num_cpu, neglect = True, normalize = normalize, notebook_name = '', suppress = True)
            data.importAndProcess()


        ## use "None"
        print('        ---------------------------------------------------')
        print('        case 2: None (only set zero_tolerance)')
        print('             2.1: set detection limit correctly?')
        print('    file_names: test_case_3.csv')
        file_names = 'emmer/data/data_dir_1/test_case_1.csv'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_lim: 1')
        upper_lim = 1
        print('    lower_lim: 1')
        lower_lim = 1
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look_1: True')
        quick_look_1 = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1

            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_1, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)

        data.importAndProcess()

        my_result = data.detection_limit
        expected_result = 0
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.2: set filter correctly?')
        my_result = data.filter
        expected_result = 'None'
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.3: remove correct features')
        my_result = list(data.filtered_data.data.columns.values)
        expected_result = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']
        self.assertListEqual(my_result, expected_result)

        ## test detection limit
        print('        ---------------------------------------------------')
        print('        case 3: set detection limits')
        print('             3.1: set detection limits correctly')
        print('    file_names: test_case_3.csv')
        file_names = 'emmer/data/data_dir_1/test_case_1.csv'
        print('    detection_limit: 10')
        detection_limit = 10
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_lim: 1')
        upper_lim = 1
        print('    lower_lim: 1')
        lower_lim = 1
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look_1: True')
        quick_look_1 = True
        print('    use_fractional_abundance: False')
        use_fractional_abundance = False
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        if os.cpu_count() > 1:
            num_cpu = os.cpu_count() - 1
            print(f'    num_cpu: {num_cpu}')
        else:
            print('    num_cpu: 1')
            num_cpu = 1
            print('    your computer only have one CPU; unable to test multiprocessing function')

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_1, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)

        data.importAndProcess()

        my_result = data.detection_limit
        expected_result = 10
        self.assertEqual(my_result, expected_result)

        print('        ---------------------------------------------------')
        print('             3.2: set detection filter correctly')
        my_result = data.filter
        expected_result = 'None'
        self.assertEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             3.3: post-filter data')
        my_result = list(data.filtered_data.data['col2'])
        expected_result = [0, 0, 10, 0, 14, 14]
        self.assertListEqual(my_result, expected_result)
        print('===========================================================')


    def test_infoRichCallingAndReproducibility(self):
        print('\ntest_Kernal.infoRichCallingAndReproducibility:')
        print('        case 1: set quick_look (args.q) as False')
        print('                before consider the maximum number of information-rich feature')
        print('    file_names: test_case_1.csv')
        file_names = 'emmer/data/test_case_1.csv'
        print('    detection_limit: 0')
        detection_limit = 0
        print('    tolerance: 1')
        tolerance = 1
        print('    filter: "None"')
        filter = 'None'
        print('    upper_lim: 1')
        upper_lim = 0.5
        print('    lower_lim: 1')
        lower_lim = 0.5
        print('    information-rich threshold: 1')
        infoRich_threshold = 1
        print('    quick_look_2: False')
        quick_look_2 = False
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_2, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)

        data.importAndProcess()
        data.infoRichCallingAndReproducibility()
        my_result = list(data.info_rich_features_w_reproducibility['feature_name'])
        expected_result = ['col1', 'col2', 'col3', 'col5', 'col4', 'col6']
        self.assertListEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('        case 2: maximum number of information-rich feature')
        print('             2.1 at quick look mode')
        print('                 ability to prevent report more information-rich feature than the maximum cap (Warning code 11)')
        print('    file_names: data/data_dir_4/group_A.csv')
        file_names = 'emmer/data/data_dir_4/group_A.csv'
        print('    detection_limit: 0.001')
        detection_limit = 0.001
        print('    tolerance: 0.33')
        tolerance = 0.33
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_lim: 2')
        upper_lim = 2
        print('    lower_lim: 0.2')
        lower_lim = 0.2
        print('    information-rich threshold: 2')
        infoRich_threshold = 2
        print('    quick_look_2: True')
        quick_look_2 = True
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_2, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)
        data.importAndProcess()
        data.infoRichCallingAndReproducibility()

        my_result = data.list_of_info_rich_features
        expected_result = ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_9', 'ASV_11', 'ASV_15', 'ASV_16', 'ASV_18', 'ASV_19', 'ASV_20', 'ASV_21', 'ASV_22', 'ASV_23']
        self.assertListEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.2 report WarningCode11')
        my_result = data.warning_code
        expected_result = '11'
        self.assertEqual(my_result, expected_result)


        ## Maximum number of information-rich feature (calculate reproducibility)
        ## also text the informaiton-rich feature calling
        print('        ---------------------------------------------------')
        print('             2.3 quick look mode off')
        print('             2.3.1 ability to prevent report more information-rich feature than the maximum cap (Warning code 11, 12)')
        print('    file_names: data/data_dir_4/group_A.csv')
        file_names = 'emmer/data/data_dir_4/group_A.csv'
        print('    detection_limit: 0.001')
        detection_limit = 0.001
        print('    tolerance: 0.33')
        tolerance = 0.33
        print('    filter: "HardFilter"')
        filter = 'HardFilter'
        print('    upper_lim: 0.2')
        upper_lim = 0.2
        print('    lower_lim: 0.2')
        lower_lim = 0.2
        print('    information-rich threshold: 2')
        infoRich_threshold = 2
        print('    quick_look_2: False')
        quick_look_2 = False
        print('    use_fractional_abundance: True')
        use_fractional_abundance = True
        print('    vNE_output_folder: ""')
        vNE_output_folder = ''
        print('    output_file_tag: out')
        output_file_tag = ''
        print('    normalize: False')
        normalize = False
        print('    num_cpu: 1')
        num_cpu = 1

        data = Kernal(file_name = file_names, detection_limit = detection_limit, tolerance = tolerance,
                      filter = filter, upper_lim = upper_lim, lower_lim = lower_lim, infoRich_threshold = infoRich_threshold,
                      quick_look = quick_look_2, use_fractional_abundance = use_fractional_abundance,
                      vNE_output_folder = vNE_output_folder, output_file_tag = output_file_tag,
                      num_cpu = num_cpu, notebook_name = '', normalize = normalize, neglect = True)
        data.importAndProcess()
        data.infoRichCallingAndReproducibility()

        my_result = list(data.info_rich_features_w_reproducibility['feature_name'])
        expected_result = ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_11', 'ASV_22', 'ASV_23', 'ASV_9', 'ASV_18', 'ASV_19', 'ASV_21', 'ASV_15', 'ASV_16', 'ASV_27']
        self.assertListEqual(my_result, expected_result)


        print('        ---------------------------------------------------')
        print('             2.3.2 report WarningCode12')
        my_result = data.warning_code
        expected_result = '12'
        self.assertEqual(my_result, expected_result)


        os.remove('test_case_1__sub_0_detail_vNE.csv')
        os.remove('test_case_1__sub_1_detail_vNE.csv')
        os.remove('test_case_1__sub_2_detail_vNE.csv')
        os.remove('test_case_1__sub_3_detail_vNE.csv')
        os.remove('test_case_1__sub_4_detail_vNE.csv')
        os.remove('test_case_1__sub_5_detail_vNE.csv')
        os.remove('group_A__detail_vNE.csv')
        os.remove('group_A__sub_0_detail_vNE.csv')
        os.remove('group_A__sub_1_detail_vNE.csv')
        os.remove('group_A__sub_2_detail_vNE.csv')
        os.remove('group_A__sub_3_detail_vNE.csv')
        os.remove('group_A__sub_4_detail_vNE.csv')
        os.remove('group_A__sub_5_detail_vNE.csv')
        os.remove('group_A__sub_6_detail_vNE.csv')
        os.remove('group_A__sub_7_detail_vNE.csv')
        os.remove('group_A__sub_8_detail_vNE.csv')
        os.remove('group_A__sub_9_detail_vNE.csv')
        os.remove('group_A__sub_10_detail_vNE.csv')
        os.remove('group_A__sub_11_detail_vNE.csv')
        os.remove('group_A__sub_12_detail_vNE.csv')
        print('===========================================================')


if __name__ == '__main__':
    unittest.main()

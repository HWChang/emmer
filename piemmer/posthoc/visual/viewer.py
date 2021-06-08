#!/usr/bin/env python3

from ...main.basic.math import NonDesityMatrix
from ...main.basic.read import RawDataImport
from ...toolbox.technical import emptyNumpyArray
from ...troubleshoot.warn.warning import WarningCode8

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas
import pylab
import numpy
import time
import sys
import os


class Projection:
    """
    Generate transformation matrix and scaler to project samples onto PCA space.
    Save those transformation matrix and scaler as attributes for easy access. Those
    attributes are important when projecting new observations onto the same PCA space.
    """

    def __init__(self, merged_dataframe, normalize):
        self.feature_names = list(merged_dataframe.columns.values)
        self.sample_id = list(merged_dataframe.index.values)
        self.data = numpy.array(merged_dataframe)
        self.df = merged_dataframe

        # get scaler (colmean)
        self.normalize = normalize
        self.non_density_matrix = NonDesityMatrix(self.data, normalize = self.normalize)

        # run normEigvals() so it will update colmean and matrixForSVD at the same time
        self.norm_eigvals = self.non_density_matrix.normEigvals()   # percent variance explained

        try:
            if len(self.norm_eigvals) < 2:
                raise Error(code = '11')
            elif len(self.norm_eigvals) == 2:
                self.plot_dimension = 2
            else:
                self.plot_dimension = 3
        except Error as e:
            if e.code == '11':
                raise ErrorCode11(suppress = False, second_chance = False) from e

        #self.scaler = self.non_density_matrix.colmean
        self.colmean = self.non_density_matrix.colmean
        self.epsilon = self.non_density_matrix.epsilon
        self.matrixForSVD = self.non_density_matrix.matrixForSVD

        u, s, vh = numpy.linalg.svd(self.matrixForSVD)

        self.Vh = vh
        self.V = numpy.transpose(vh[0:len(s),:])
        ## vh:
        #     row: principal components; col: features
        ## V:
        #     row: features; col: principal components

        self.U = u
        ## v:
        #     row: sample; col: principal components

        self.S = numpy.diag(s)
        ## s

        ncol_V = numpy.size(self.V, 1)
        self.PC_list = list(['PC' + str(i) for i in range(1 , (ncol_V + 1))])

        self.colmean_df = pandas.DataFrame([self.colmean], columns = self.feature_names, index = ['colmean'])
        self.V_df = pandas.DataFrame(self.V, columns = self.PC_list[0:len(s)], index = self.feature_names)

        nrow = numpy.size(self.data, 0)
        mean_centered_matrix = self.data - numpy.tile(self.colmean, (nrow, 1))

        if normalize == True:
            self.colstd = self.non_density_matrix.colstd
            self.colstd_df = pandas.DataFrame([self.colstd], columns = self.feature_names, index = ['colstd'])
            scaled_mean_centered_matrix = numpy.matmul(mean_centered_matrix, numpy.diag(1/self.colstd))
            projection = numpy.matmul(scaled_mean_centered_matrix, self.V)
        else:
            projection = numpy.matmul(mean_centered_matrix, self.V)

        self.projection_df = pandas.DataFrame(projection, columns = self.V_df.columns.values, index = self.sample_id)

        # for annotating PCA plot
        self.PC_annotation = pandas.DataFrame(data = emptyNumpyArray(nrow = len(self.norm_eigvals), ncol = 3),
                                              columns=['PC', 'percent explain', 'PC w percent explain'])
        self.PC_annotation['PC'] = self.PC_list
        self.PC_annotation['percent explain'] = list([numpy.round(i * 100, 2)for i in self.norm_eigvals])
        self.PC_annotation['PC w percent explain'] = self.PC_annotation["PC"].astype(str) + ' (' + self.PC_annotation['percent explain'].astype(str) + '%)'


    def cleanSpec(self):
        """
        If the input matrix can be decomposed by SVD into a spectrum of matrices, this function
        will clean the spectrum and only retain the matrices that corresponding to PC1, PC2, and,
        if available, PC3. Then this function will sum all of those matrices together and obtain
        a new matric that call self.spec_cleaned_data
        """
        S_select = pandas.DataFrame(self.S[:, 0:self.plot_dimension])
        S_zero = pandas.DataFrame(numpy.zeros([self.df.shape[0], (self.df.shape[1] - self.plot_dimension)]))
        S_adj = pandas.concat([S_select, S_zero], axis = 1, sort = True)
        self.S_adj = numpy.nan_to_num(S_adj)   # convert nan to 0

        U_times_S = numpy.matmul(self.U , self.S_adj)
        self.spec_cleaned_data = numpy.matmul(U_times_S , self.Vh)


class Plot:
    """
    Generate 2D or 3D PCA plot. Allow user to decide the best angle to present the PCA for best
    visualization experience.
    """

    def __init__(self, Projection_class_in_list, input_file_in_list_of_list, output_file_name, filter):#, PC_annotation_in_list):
        self.Projection_class_in_list = Projection_class_in_list
        self.input_file_in_list_of_list = input_file_in_list_of_list
        self.output_file_name = output_file_name
        self.filter = filter
        #self.PC_annotation_in_list = PC_annotation_in_list


    def extractData(self, current_dataset):
        # update self.current_dataset
        self.current_dataset = current_dataset

        # extract data
        self.current_coordinates = self.Projection_class_in_list[self.current_dataset].projection_df
        self.current_PC_list = self.Projection_class_in_list[self.current_dataset].PC_list
        self.current_PC_list_annotation = self.Projection_class_in_list[self.current_dataset].PC_annotation
        self.current_percent_explain = numpy.round((numpy.array(self.Projection_class_in_list[self.current_dataset].norm_eigvals) * 100), decimals = 2)

        self.current_dataset = 0 # reset iteration
        self.current_group = [os.path.basename(element).replace(".csv", "") for element in self.input_file_in_list_of_list[self.current_dataset]]


    def projectDots2D(self):
        """
        add dots on a 2D plot
        """
        for i in range(len(self.current_group)):
            self.projection_df_subset = self.current_coordinates[[self.current_group[i] in rowname for rowname in self.current_coordinates.index]]

            x = self.projection_df_subset['PC1']
            y = self.projection_df_subset['PC2']

            #add dots onto the plot
            self.ax.scatter(x, y, label = self.current_group[i], alpha = 1)

            self.ax.set_xlabel(self.current_PC_list[0] + ' (' + str(self.current_percent_explain[0]) + '%)')
            self.ax.set_ylabel(self.current_PC_list[1] + ' (' + str(self.current_percent_explain[1]) + '%)')

            self.ax.set_xlabel(self.current_PC_list_annotation['PC w percent explain'][0])
            self.ax.set_ylabel(self.current_PC_list_annotation['PC w percent explain'][1])


    def projectDots3D(self):
        """
        add dots on a 3D plot
        """
        for i in range(len(self.current_group)):
            self.projection_df_subset = self.current_coordinates[[self.current_group[i] in rowname for rowname in self.current_coordinates.index]]

            x = self.projection_df_subset['PC1']
            y = self.projection_df_subset['PC2']
            z = self.projection_df_subset['PC3']

            #add dots onto the plot
            self.ax.scatter(x, y, z, label = self.current_group[i], alpha = 1)   #

            self.ax.set_xlabel(self.current_PC_list[0] + ' (' + str(self.current_percent_explain[0]) + '%)')
            self.ax.set_ylabel(self.current_PC_list[1] + ' (' + str(self.current_percent_explain[1]) + '%)')
            self.ax.set_zlabel(self.current_PC_list[2] + ' (' + str(self.current_percent_explain[2]) + '%)')

            self.ax.set_xlabel(self.current_PC_list_annotation['PC w percent explain'][0])
            self.ax.set_ylabel(self.current_PC_list_annotation['PC w percent explain'][1])
            self.ax.set_zlabel(self.current_PC_list_annotation['PC w percent explain'][2])


    def assembleSubPlot(self, current_dataset, plot_location, title):
        self.extractData(current_dataset)

        try:
            if len(self.current_percent_explain) < 2:
                raise Error(code = '11')
            elif len(self.current_percent_explain) == 2:
                self.ax = self.fig.add_subplot(plot_location)
                self.projectDots2D()
            else:
                self.ax = self.fig.add_subplot(plot_location, projection='3d')
                self.projectDots3D()
        except Error as e:
            raise ErrorCode11(suppress = False) from e

        self.ax.legend(loc = 'upper right')
        self.ax.set_title(title)


    def viewSinglePCAplot(self, current_dataset = 0, plot_location = '111', title = ''):
        """
        Assemble a PCA plot
        """
        self.fig = plt.figure()

        self.assembleSubPlot(current_dataset = 0, plot_location = plot_location, title = title)
        self.ax.legend(loc = 'upper right')

        plt.show()

        # TODO:
        # ref: https://stackoverflow.com/questions/23424282/how-to-get-azimuth-and-elevation-from-a-matplotlib-figure
        self.fig.savefig(self.output_file_name, idp = 300)


    def viewSanityCheckPlots(self):
        """
        Generate plots for sanity check
        """
        if self.filter != 'None':
            self.fig = plt.figure()

            self.assembleSubPlot(current_dataset = 0, plot_location = '231', title = 'Unfiltered')
            self.assembleSubPlot(current_dataset = 1, plot_location = '232', title = 'filtered out')
            self.assembleSubPlot(current_dataset = 2, plot_location = '233', title = 'filtered')
            self.assembleSubPlot(current_dataset = 3, plot_location = '234', title = 'filtered;\nnon-infoRich')
            self.assembleSubPlot(current_dataset = 4, plot_location = '235', title = 'filtered;\ninfoRich')
            self.assembleSubPlot(current_dataset = 5, plot_location = '236', title = 'non-infoRich')

            plt.show()
            self.fig.savefig(self.output_file_name, idp = 300)

        else:
            self.fig = plt.figure()

            self.assembleSubPlot(current_dataset = 0, plot_location = '131', title = 'Unfiltered')
            self.assembleSubPlot(current_dataset = 1, plot_location = '132', title = 'non-infoRich')
            self.assembleSubPlot(current_dataset = 2, plot_location = '133', title = 'infoRich')

            plt.show()
            self.fig.savefig(self.output_file_name, idp = 300)


        # TODO: Add force_2D option
        #       Provent mixed 3D and 2D plots in sanity check plot


class RetrospectPlot:
    """
    Generate 2D or 3D PCA plot for retrospect module
    """

    def __init__(self, coordinate_and_setting_df, dimension, level, output_file_name, PC_annotation):
        self.coordinate_and_setting_df = coordinate_and_setting_df
        self.dimension = dimension
        self.level = level
        self.output_file_name = output_file_name
        self.PC_annotation = PC_annotation

    def plot(self):
        fig = plt.figure()

        if self.dimension == '3D':
            ax = fig.add_subplot(111, projection='3d')
        elif self.dimension == '2D':
            ax = fig.add_subplot(111)

        x = self.coordinate_and_setting_df['PC1']
        y = self.coordinate_and_setting_df['PC2']
        fc = list(self.coordinate_and_setting_df['fill_color'])
        ec = list(self.coordinate_and_setting_df['edge_color'])
        s = list(self.coordinate_and_setting_df['shape'])
        if self.dimension == '3D':
            z = self.coordinate_and_setting_df['PC3']

        ## why it does not work:
        #  ref: https://github.com/matplotlib/matplotlib/issues/11155
        # TODO: track this issue; for now; please manually change the setting and import by -p
        # TODO: add a WarningCode to notify user
        try:
            if list(set(s)) != ['o']:
                 raise WarningCode8(silence = False)
        except:
            pass

        if self.dimension == '3D':
            ax.scatter(x, y, z, facecolors = fc, edgecolors = ec,# marker = str(s),
                       label = self.coordinate_and_setting_df[self.level], alpha = 1)
        else:
            ax.scatter(x, y, facecolors = fc, edgecolors = ec,# marker = str(s),
                       label = self.coordinate_and_setting_df[self.level], alpha = 1)

        if isinstance(self.PC_annotation, pandas.DataFrame):
            ax.set_xlabel(self.PC_annotation['PC w percent explain'][0])
            ax.set_ylabel(self.PC_annotation['PC w percent explain'][1])
            if self.dimension == '3D':
                ax.set_zlabel(self.PC_annotation['PC w percent explain'][2])
        else:
            ax.set_xlabel('PC1')
            ax.set_ylabel('PC2')
            if self.dimension == '3D':
                ax.set_zlabel('PC3')

        plt.show()
        fig.savefig(self.output_file_name, idp = 300)

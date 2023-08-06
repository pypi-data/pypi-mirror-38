import os
import time
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from sklearn import linear_model
from statsmodels.api.tsa import VARMAX
import pickle
from AngelEncoder import AngelEncoder
import tensorflow as tf
tf.enable_eager_execution()

class DataModel():
    """
    DataModel

    [A parent class for the linear and nonlinear models we implement for
    high-dimensional time series data.]

    :return: [description]
    :rtype: [type]
    """


    def __init__(self, name, lags=1, windowsize=1, endog=True):
        super().__init__()
        self._name = name
        self._lags = lags
        self._windowsize = windowsize
        self._endog = endog
        self._dimensions = None

    #----------- Getters & Setters ------------- #
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname: str):
        if not isinstance(newname, str):
            raise ("Name needs to be a string.")
        self._name = newname

    @property
    def lags(self):
        return self._lags

    @lags.setter
    def lags(self, newlags: int):
        if not isinstance(newlags, int):
            raise TypeError("Lags need to be an integer.")
        self._lags = newlags

    @property
    def dimensions(self):
        try:
            self._dimensions = self.df.shape
        except:
            self._dimensions = None
        return self._dimensions
    # @dimensions.setter
    # def dimensions(self, newdimensions: int):
    #     if not isinstance(newdimensions, int):
    #         raise TypeError("Needs to be an integer.")
    #     self._dimensions = newdimensions

    @property
    def windowsize(self):
        return self._windowsize

    @windowsize.setter
    def windowsize(self, newwindowsize: int):
        if not isinstance(newwindowsize, int):
            raise TypeError("Needs to be an integer.")
        self._windowsize = newwindowsize

    @property
    def endog(self):
        return self._endog

    @endog.setter
    def endog(self, newendog: bool):
        if not isinstance(newendog, bool):
            raise TypeError("Needs to be a boolean")
        self._endog = newendog

    # ----- Getters & Setters ------- #

#---------------Functions-----------------------#

    def read(self, file: str, header: int = 0, matField: str = 'data'):

        """Reads a CSV to a Pandas array

        :rtype: pdarray

        :raises: FileError -- if not .csv file

        :warning: Must be a string as a filepath

        """

        with open (file, 'r') as f:
            if ".csv" in file:
                print("Opening CSV file...")
                self.df = pd.read_csv(file, header=header).values
                print("CSV read!")
            elif ".mat" in file:
                print("Opening .mat file")
                self.df = sio.loadmat(file)[matField]
                if self.df is not None:
                    print(".mat file loaded!")
                else:
                    raise FileNotFoundError("Please try again")
            else:
                raise FileNotFoundError("Please try again, using an appropriate file type.")

        # self.dimensions.extend(list(self.df.shape))

    def show(self):
        if self.df is not None:
            return self.df
        else:
            raise FileNotFoundError("Cannot find dataframe to display")


    def destroy(self):
        if self.df is not None:
            del self.df
        else:
            raise FileNotFoundError("Cannot find dataframe to destroy")

            
    def save(self, savename = None):

        """Saves Pandas array to pickle file for retrieval at a later date.

        Function takes two arguments, initially the dataframe to save, and then the filename to save as.

        TODO it might be worth adding in an optional file keyword argument to this function to allow for people \
        working with multiple DFs in the same session to specify which gets pickled?

        TODO Change .pkl to something else because cannot save Angel Encoder - all models other than AE can be saved to .pkl\
        this might require joblib.dump() or something

        :rtype: Pickle file (.pkl)

        """

        if savename is None:
            savename = input("Enter a filename to save as: ")
        self.pickledfile = self.df.to_pickle("{}.{}.pkl".format(savename, time.strftime("%Y%m%d-%H%M%S")))


    def plot(self):
        plt.plot(self.df)
        plt.savefig(str(self.df) + '.png')
        plt.show()


    def slice(self):
        self.slicedwindows = np.swapaxes(np.dstack(self.df[i:1+i-self._windowsize or None:self._lags] for i in range(0, self._windowsize)), 1, 2)
        # [self.df[i:i+self._windowsize] for i in range(0, self.df.shape[0], self._windowsize)]

    # def window_slicer(data, stepsize=24, width=238):
    #     return np.swapaxes(np.dstack(data[i:1+i-width or None:stepsize] for i in range(0,width)), 1, 2)

    def AE(self):
        data = sio.loadmat('/Users/alexharston/Desktop/S1_Bedroom.mat')['data'].astype(np.uint8)
        data = window_slicer(data)
        AE = AngelEncoder(dataFormat='channels_first', endoLayer=3, filters=[3,4,5], kernelSizes=(8,80), optimiser=tf.train.AdamOptimizer)
        AE.fit(data, tf.train.get_or_create_global_step())
        print(AE)

    def VARMAX(self):
        self.varmax = VARMAX(self.data, order=(2, 0), trend='nc', exog=exog)
        self.res = self.varmax.fit(maxiter=1000, disp=False)
        print(self.res.summary())

if __name__ == "__main__":
    #Parser instantiation and definition
    parser = argparse.ArgumentParser(description="PypeLearn - a framework for \
    processing machine learning time series datastreams (VARMAX, NARX, \
    Linear Regression and Gaussian Process Models) and automating \
    step-wise predictions and automated graphs")

    #Adds the arguments
    parser.add_argument("name", help='Name of Model')
    parser.add_argument("--file", "-f", help="Select file")
    parser.add_argument("--windowsize", "-w", help="Size of the moving average \
                        window size", type=int)

    args = parser.parse_args()
    dm = DataModel(args.name)

    if args.file:
        dm.read(args.file)
        print(dm.show())

    if args.windowsize:
        dm._windowsize = args.windowsize
        print("Window Size: ", dm._windowsize)

    tf.app.run()

##########################################################################
class NARX(DataModel):

    """
     NARX

    [Subclasses DataModel]

    :raises TypeError: [If input nodes are not ``int``]
    :return: [description]
    :rtype: [type]
    """


    def __init__(self, name, lags=1, dimensions=1, windowsize=1, input_nodes=0,
                hidden_nodes=0, output_nodes=0):
        super().__init__(name, lags, dimensions, windowsize)

        self._input_nodes = input_nodes
        self._hidden_nodes = hidden_nodes
        self._output_nodes = output_nodes

    # ------- Getters and Setters -------- #
    @property
    def input_nodes(self):
        return self._input_nodes


    @input_nodes.setter
    def input_nodes(self, newinput_nodes):
        if not isinstance(newinput_nodes, int):
            raise TypeError("Needs to be an integer.")
        self._input_nodes = newinput_nodes


    @property
    def hidden_nodes(self):
        return self._hidden_nodes


    @hidden_nodes.setter
    def hidden_nodes(self, newhidden_nodes):
        if not isinstance(newhidden_nodes, int):
            raise TypeError("Needs to be an integer.")
        self._hidden_nodes = newhidden_nodes


    @property
    def output_nodes(self):
        return self._output_nodes


    @output_nodes.setter
    def output_nodes(self, newoutput_nodes):
        if not isinstance(newoutput_nodes, int):
            raise TypeError("Needs to be an integer.")
        self._output_nodes = newoutput_nodes

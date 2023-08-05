import pandas as pd
from scipy.stats import percentileofscore

class Distribution:

    def __init__(self, mu=0, sigma=1):
        """ Generic distribution class for calculating and
        visualizing a probability distribution.

        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard deviation of the distribution
            data (list of floats) a list of floats extracted from the data file

        """

        self.mean = mu
        self.stdev = sigma
        self.data = []

    def calculate_percentile(self, x):
        """ Given a point on a distribution, get its percentile rank

        Arg:
            x (float): a point whose percentile rank we desire

        Returns:
            (float): the percentile rank

        """

        rank = percentileofscore(self.data, x)

        return rank

    def read_data_file(self, file_name, file_type='csv'):
        """Function to read in data from a file. The file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            file_name (string): name of a file to read from
            file_type (string): file extension, one of 'csv' or 'txt'

        Returns:
            None

        """

        if file_type == 'txt':
            with open(file_name) as file:
                data_list = []
                line = file.readline()
                while line:
                    data_list.append(int(line))
                    line = file.readline()
            file.close()

        if file_type == 'csv':
            data = pd.read_csv(file_name, header = None)
            data_list = data.iloc[:,0].values.tolist()

        self.data = data_list

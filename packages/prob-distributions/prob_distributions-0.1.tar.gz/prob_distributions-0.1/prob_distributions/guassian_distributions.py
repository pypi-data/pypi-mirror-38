import math
import matplotlib.pyplot as plt
from .general_distributions import Distribution

class Guassian(Distribution):

    """ Gaussian distribution class for calculating and
	visualizing a Gaussian distribution.

	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats extracted from the data file

	"""

    def __init__(self, mu = 0, sigma = 1):
        Distribution.__init__(self, mu, sigma)

    def read_data_file(self, filename, sample = True):

        """Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute
        also this function updates the mean and stdev Attributes based on the
        data read in.

		Args:
			file_name (string): name of a file to read from
            sample (bool): whether the data represents a sample or population

		Returns:
			None

		"""

        with open(filename) as file:
            line = file.readline()
            data_list = []

            while(line):
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev(sample)

    def calculate_mean(self):

        """Function to calculate the mean of the data set.

		Args:
			None

		Returns:
			float: mean of the data set

		"""

        self.mean = 1.0 * (sum(self.data)/len(self.data))
        return self.mean

    def calculate_stdev(self, sample = True):

        """Function to calculate the standard deviation of the data set.

		Args:
			sample (bool): whether the data represents a sample or population

		Returns:
			float: standard deviation of the data set

		"""

        if(sample):
            n = len(self.data)-1
        else:
            n = len(self.data)

        sigma = 0
        for d in self.data:
            sigma += (d - self.mean)**2

        self.stdev = math.sqrt(sigma/n)
        return self.stdev

    def plot_histogram(self):

        """Function to output a histogram of the instance variable data using
		matplotlib pyplot library.

		Args:
			None

		Returns:
			None
		"""

        plt.hist(self.data)
        plt.title("Histogram of data")
        plt.xlabel("Data")
        plt.ylabel("Count")

    def pdf(self,x):

        """Probability density function calculator for the gaussian distribution.

		Args:
			x (float): point for calculating the probability density function


		Returns:
			float: probability density function output
		"""

        return  (1.0/math.sqrt(2*math.pi*math.pow(self.stdev,2))) * math.exp(-1 * (math.pow((x-self.mean),2)/(2*math.pow(self.stdev,2))))

    def plot_histogram_pdf(self, n_bins = 50):

        """Function to plot the normalized histogram of the data and a plot of the
		probability density function along the same range

		Args:
			n_bins (int): number of data points

		Returns:
			list: x values for the pdf plot
			list: y values for the pdf plot

		"""

        x_min = min(self.data)
        interval = 1.0 * ((max(self.data) - x_min)/n_bins)

        x = []
        y = []

        for i in range(n_bins+1):
            x_val = x_min + (i * interval)
            x.append(x_val)
            y.append(self.pdf(x_val))

        fig,axes = plt.subplots(2,1,sharex = True)
        axes[0].hist(self.data, density = True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x,y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[1].set_ylabel('Density')

        return x,y

    def __add__(self, other):

        """Function to add together two Gaussian distributions

		Args:
			other (Gaussian): Gaussian instance

		Returns:
			Gaussian: Gaussian distribution

		"""

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(math.pow(self.stdev,2) + math.pow(other.stdev,2))
        return result

    def __repr__(self):

        """Function to output the characteristics of the Gaussian instance

		Args:
			None

		Returns:
			string: characteristics of the Gaussian

		"""

        return "mean: {}, standard deviation: {}".format(self.mean, self.stdev)

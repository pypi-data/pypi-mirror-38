import math
from math import factorial as fct
import matplotlib.pyplot as plt
from .general_distributions import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) number of trials

    """
    def __init__(self, prob = 0.5, size = 20):

        self.p = prob
        self.n = size
        Distribution.__init__(self, mu=self.calculate_mean(), sigma=self.calculate_stdev())

    def calculate_mean(self):

        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """
        return self.p * self.n

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        return math.sqrt(self.n * self.p * (1 - self.p))

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """
        self.n = 1.0 * len(self.data)

        if self.n > 0.0:
            self.p = sum(self.data) / self.n
        else:
            self.p = 0.0

        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        plt.bar(x=[0, 1], height=[(len(self.data) - sum(self.data)), sum(self.data)])
        plt.xlabel("Events")
        plt.ylabel("Frequency")
        plt.xticks([0, 1])
        plt.title("Non-Event vs Event Frequncy - Binomial Distribution")


# TODO: Calculate the probability density function of the binomial distribution
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """
        n = self.n
        p = self.p

        return (1.0 * ((fct(n) / (fct(k) * fct(n - k))) * (p**k) * ((1 - p)**(n - k))))



# write a method to plot the probability density function of the binomial distribution
    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """
        x = []
        y = []
        for i in range(len(self.data)):
            x.append(i)
            y.append(self.pdf(i))

        plt.bar(x, y)
        plt.xlabel("Number of Events")
        plt.ylabel("Frequency")
        plt.xticks(x)
        plt.title("Probability Density Function - Binomial Distribution")

        return x, y

# write a method to output the sum of two binomial distributions. Assume both distributions have the same p value.
    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """
        try:
            assert self.p == other.p, 'p values are equal'
        except AssertionError as error:
            print("Sorry, to add 2 binominal class instances prob values of both the instances should be the same")
            # raise

        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.mean = result.calculate_mean()
        result.stdev = result.calculate_stdev()
        return result

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)

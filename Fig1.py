import math
import pylab
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

def nash_calculator_cobb_douglas_homogeneous(w_values, beta, a, c, alpha, n):
    exponent_param = 1 / (1 - beta)
    exponent_w = alpha * exponent_param
    aggregation_g = sum(w ** (alpha / (1 - beta)) for w in w_values)
    # calculate public good
    common_public_good = (((beta * (a + c)) ** exponent_param) * aggregation_g) / (a + (c * n))
    # individual public good amounts
    q_ = (((beta * (a + c)) ** exponent_param) * (
            np.array(w_values) ** (alpha / (1 - beta))) - c * common_public_good) / a
    if np.any(q_ < 0):
        # q_[q_ < 0] = 0
        q_[1] = 0
        q_[0] = (((beta * (a + c)) ** exponent_param) * ((w_values[0]) ** exponent_w)) / (a + c)
        common_public_good = q_[0]
    total_public_good = [(a * q + c * common_public_good) for q in q_]
    # welfare
    pi = (np.array(w_values) ** alpha) * ((np.array(total_public_good)) ** beta) - np.array(q_)
    sum_pi = sum(pi)
    return common_public_good, q_, sum_pi, pi


def main():
    # Parameters
    beta = 0.4
    alpha = 0.4
    n = 2
    a = 1
    c = 1
    wealth = np.array([5000, 500])
    wealth_2 = np.array([5000, 5000])

    initial_values = [0.1, 0.1]
    bounds = (0, None)
    bounds_q = (bounds, bounds)

    # increments
    initial_delta = 5  # Initial value of delta
    delta_increment = 5  # Fixed increment for delta
    num_deltas = 200 # Number of different delta values
    # the lists
    average_wealth = []
    average_wealth_2 =[]
    # welfare denoted by relative amounts for nash
    rw_good_contribution = []
    rw_good_nash_1 = []
    rw_good_nash_2 = []
    rw_welfare_1_nash = []
    rw_welfare_2_nash = []

    #only for Fig 1, second subplot: the arrays corresponding to wealth_2
    rw_good_contribution_2 = []
    rw_good_nash_1_2 = []
    rw_good_nash_2_2 = []

    for i in range(num_deltas):
        # Calculate delta based on the current iteration
        delta = initial_delta + (i * delta_increment)

        # Create a new distribution by adding delta to each income
        new_distribution = wealth + delta
        new_distribution_2 = wealth_2 + delta

        w_1 = new_distribution[0]
        w_2 = new_distribution[1]

        w1_2 = new_distribution_2[0]
        w2_2 = new_distribution_2[1]

        sum_wealth = w_1 + w_2
        sum_wealth_2 = w1_2 + w2_2
        w_relative = [v / sum_wealth for v in new_distribution]
        w_relative_2 = [v / sum_wealth_2 for v in new_distribution_2]
        # Calculate the average income and append it to the list
        average = np.mean(new_distribution)
        average_2 = np.mean(new_distribution_2)

        # Calculate the amount of the public good of the distribution
        (rw_public_good_nash_homo, rw_individual_contribution_nash_homo, rw_profit_nash_homo,
         rw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(w_relative, beta, a, c, alpha, n)
        (rw_public_good_nash_homo_2, rw_individual_contribution_nash_homo_2, rw_profit_nash_homo_2,
         rw_ind_profit_nash_homo_2) = nash_calculator_cobb_douglas_homogeneous(w_relative_2, beta, a, c, alpha, n)


        # Add the list of values to the plot
        average_wealth.append(average)
        average_wealth_2.append(average_2)


        # relative wealth
        rw_good_contribution.append(rw_public_good_nash_homo)
        rw_welfare_1_nash.append(rw_ind_profit_nash_homo[0])
        rw_welfare_2_nash.append(rw_ind_profit_nash_homo[1])
        rw_good_nash_1.append(rw_individual_contribution_nash_homo[0])
        rw_good_nash_2.append(rw_individual_contribution_nash_homo[1])

        rw_good_contribution_2.append(rw_public_good_nash_homo_2)
        rw_good_nash_1_2.append(rw_individual_contribution_nash_homo_2[0])
        rw_good_nash_2_2.append(rw_individual_contribution_nash_homo_2[1])

    # Plot the graph
    rcParams.update({'figure.autolayout': True})

    # Create subplots

    # Example 1
    # Plot the first subplot
    fig1, axs1 = plt.subplots(3,2)
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 1: Decreasing public good provision with non-contributors')
    #fig1.suptitle('Nash public good levels with initial wealths: [5000, 500]')

    axs1[0,0].plot(average_wealth, rw_good_contribution, label='Relative Wealth', color='black', marker='o')
    axs1[0,0].set_title('Total Public Good')
    axs1[0,0].set_xlabel('Average total group wealth')
    axs1[0,0].set_ylabel('$Q^*$')

    axs1[1,0].plot(average_wealth, rw_good_nash_1, label='Relative Wealth', color='red', marker='o')
    axs1[1,0].set_title('Contribution of Country 1')
    axs1[1,0].set_xlabel('Average total group wealth')
    axs1[1,0].set_ylabel('$q_1^*$')

    axs1[2,0].plot(average_wealth, rw_good_nash_2, label='Relative Wealth', color='blue', marker='o')
    axs1[2,0].set_title('Contribution of Country 2')
    axs1[2,0].set_xlabel('Average total group wealth')
    axs1[2,0].set_ylabel('$q_2^*$')

    axs1[0,1].plot(average_wealth_2, rw_good_contribution_2, label='Relative Wealth', color='black', marker='o')
    axs1[0,1].set_title('Total Public Good')
    axs1[0,1].set_xlabel('Average total group wealth')
    axs1[0,1].set_ylabel('$Q^*$')

    axs1[1,1].plot(average_wealth_2, rw_good_nash_1_2, label='Relative Wealth', color='red', marker='o')
    axs1[1,1].set_title('Contribution of Country 1')
    axs1[1,1].set_xlabel('Average total group wealth')
    axs1[1,1].set_ylabel('$q_1^*$')

    axs1[2,1].plot(average_wealth_2, rw_good_nash_2_2, label='Relative Wealth', color='blue', marker='o')
    axs1[2,1].set_title('Contribution of Country 2')
    axs1[2,1].set_xlabel('Average total group wealth')
    axs1[2,1].set_ylabel('$q_2^*$')

    # Adjust layout
    plt.tight_layout()

    # Add title
    # plt.title('Increasing wealth of all countries, alpha = 0.4, beta = 0.4')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()

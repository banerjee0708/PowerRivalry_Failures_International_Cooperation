import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy.optimize import minimize


def welfare_social_optimum_q(w1, w2, a, c, beta, alpha):
    def welfare_fun(q):
        q1, q2 = q
        public_good_1 = a * q1 + c * (q1 + q2)
        public_good_2 = a * q2 + c * (q1 + q2)
        pi_1 = (w1 ** alpha) * (public_good_1 ** beta) - q1
        pi_2 = (w2 ** alpha) * (public_good_2 ** beta) - q2
        pi = pi_1 + pi_2
        return - pi

    return welfare_fun


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
    initial_values = [0.1, 0.1]
    bounds = (0, None)
    bounds_q = (bounds, bounds)
    wealth = np.array([5000, 5000])
    # increments
    initial_delta = 5  # Initial value of delta
    delta_increment = 5  # Fixed increment for delta
    num_deltas = 500  # Number of different delta values
    # the lists
    average_wealth = []
    iteration = []
    average_cost = []
    # welfare denoted by total amounts for nash
    aw_good_contribution = []
    aw_welfare_1_nash = []
    aw_welfare_2_nash = []
    aw_sum_welfare_nash = []
    # welfare denoted by total amounts for soc planner
    aw_soc_optimum = []
    aw_sum_welfare_soc = []
    # welfare denoted by relative amounts for nash
    rw_good_contribution = []
    rw_good_nash_1 = []
    rw_good_nash_2 = []
    rw_welfare_1_nash = []
    rw_welfare_2_nash = []
    rw_sum_welfare_nash = []
    # welfare denoted by relative amounts for soc planner
    rw_soc_optimum = []
    rw_sum_welfare_soc = []

    # diff b/w nash and social optimum
    diff_soc_nash_aw = []
    diff_soc_nash_rw = []
    diff_abs_soc_nash = []

    for i in range(num_deltas):
        # Calculate delta based on the current iteration
        delta_1 = initial_delta + (i * delta_increment)
        delta_2 = initial_delta + (i * delta_increment)

        # Create a new distribution by adding delta to each income
        # new_distribution = wealth + delta
        new_distribution = [wealth[0] +  delta_1, wealth[1] + 2 * delta_2]

        w_1 = new_distribution[0]
        w_2 = new_distribution[1]

        sum_wealth = w_1 + w_2
        w_relative = [v / sum_wealth for v in new_distribution]
        # Calculate the average income and append it to the list
        average = np.mean(new_distribution)
        # social planners optimization
        solution_absolute = minimize(welfare_social_optimum_q(wealth[0], wealth[1], a, c, beta, alpha), (0, 0),
                                     method="trust-constr", bounds=bounds_q)
        solution_relative = minimize(welfare_social_optimum_q(w_relative[0], w_relative[1], a, c, beta, alpha), (0, 0),
                                     method="trust-constr", bounds=bounds_q)
        aw_social_optimum = solution_absolute.x
        rw_social_optimum = solution_relative.x
        f_max_absolute = -solution_absolute.fun
        f_max_relative = -solution_relative.fun
        # Calculate the amount of the public good of the distribution
        (aw_public_good_nash_homo, aw_individual_contribution_nash_homo, aw_profit_nash_homo,
         aw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(new_distribution, beta, a, c, alpha, n)
        (rw_public_good_nash_homo, rw_individual_contribution_nash_homo, rw_profit_nash_homo,
         rw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(w_relative, beta, a, c, alpha, n)

        aw_soc_opt = sum(aw_social_optimum)
        rw_soc_opt = sum(rw_social_optimum)

        # diff soc nash
        diff_soc_nash = (f_max_relative - rw_profit_nash_homo) / rw_profit_nash_homo
        diff_absolute = f_max_relative - rw_profit_nash_homo
        aw_soc_optimum.append(aw_soc_opt)
        rw_soc_optimum.append(rw_soc_opt)
        # Add the list of values to the plot
        average_wealth.append(average)
        iteration.append(i)
        rw_sum_welfare_soc.append(f_max_relative)

        # absolute wealth - nash
        aw_good_contribution.append(aw_public_good_nash_homo)
        aw_welfare_1_nash.append(aw_ind_profit_nash_homo[0])
        aw_welfare_2_nash.append(aw_ind_profit_nash_homo[1])
        aw_sum_welfare_nash.append(aw_profit_nash_homo)
        # relative wealth
        rw_good_contribution.append(rw_public_good_nash_homo)
        rw_welfare_1_nash.append(rw_ind_profit_nash_homo[0])
        rw_welfare_2_nash.append(rw_ind_profit_nash_homo[1])
        rw_good_nash_1.append(rw_individual_contribution_nash_homo[0])
        rw_good_nash_2.append(rw_individual_contribution_nash_homo[1])
        # small edit
        rw_sum_soc = sum(rw_ind_profit_nash_homo)
        rw_sum_welfare_nash.append(rw_sum_soc)

        # welfare

        # rw_sum_welfare_nash.append(rw_profit_nash_homo)
        # (soc - nash)/nash
        diff_soc_nash_rw.append(diff_soc_nash)
        diff_abs_soc_nash.append(diff_absolute)

    # Plot the graph
    rcParams.update({'figure.autolayout': True})

    # Create subplots

    # Example 1
    # Plot the first subplot
    fig1, axs1 = plt.subplots(3)
    fig1.suptitle('Nash public good levels with initial wealths: [5000, 5000]')

    axs1[0].plot(iteration, rw_good_contribution, label='Relative Wealth', color='black', marker='o')
    axs1[0].set_title('Total Public Good')
    axs1[0].set_xlabel('Iteration')
    axs1[0].set_ylabel('$Q^*$')

    axs1[1].plot(iteration, rw_good_nash_1, label='Relative Wealth', color='red', marker='o')
    axs1[1].set_title('Contribution of Country 1')
    axs1[1].set_xlabel('Iteration')
    axs1[1].set_ylabel('$q_1^*$')

    axs1[2].plot(iteration, rw_good_nash_2, label='Relative Wealth', color='blue', marker='o')
    axs1[2].set_title('Contribution of Country 2')
    axs1[2].set_xlabel('Iteration')
    axs1[2].set_ylabel('$q_2^*$')

    # Adjust layout
    plt.tight_layout()

    # Add title
    # plt.title('Increasing wealth of all countries, alpha = 0.4, beta = 0.4')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()

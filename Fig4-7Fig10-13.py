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
        pi_1 = ((w1 ** alpha) * (public_good_1 ** beta)) - q1
        pi_2 = ((w2 ** alpha) * (public_good_2 ** beta)) - q2
        pi = pi_1 + pi_2
        return - pi

    return welfare_fun


def welfare_social_optimum_het(w1, w2, a, c_values, beta, alpha):
    def welfare_fun(q):
        q1, q2 = q
        public_good_1 = a * q1 + c_values[0] * (q1 + q2)
        public_good_2 = a * q2 + c_values[1] * (q1 + q2)
        pi_1 = ((w1 ** alpha) * (public_good_1 ** beta)) - q1
        pi_2 = ((w2 ** alpha) * (public_good_2 ** beta)) - q2
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
        q_[1] = 0
        q_[0] = (((beta * (a + c)) ** exponent_param) * ((w_values[0]) ** exponent_w)) / (a + c)
        common_public_good = q_[0]
    total_public_good = [(a * q + c * common_public_good) for q in q_]
    # welfare
    pi = (np.array(w_values) ** alpha) * ((np.array(total_public_good)) ** beta) - np.array(q_)
    sum_pi = sum(pi)
    return common_public_good, q_, sum_pi, pi


def nash_calculator_cobb_douglas_heterogeneous(w_values, beta, a, c_values, alpha, n):
    exponent_param = 1 / (1 - beta)
    exponent_w = alpha * exponent_param
    pairwise = [((beta * (a + c)) ** exponent_param) * (w ** exponent_w) for c, w in zip(c_values, w_values)]
    # calculate public good
    common_public_good = sum(pairwise) / (a + sum(c_values))  # Q = sum of z_i/(a +nc)
    # individual public good amounts
    q_ = [((((beta * (a + c)) ** exponent_param) * (w ** exponent_w)) - (c * common_public_good)) / a for
          c, w in zip(c_values, w_values)]
    q_ = np.array(q_)
    if np.any(q_ <= 0):
        q_[1] = 0
        q_[0] = (((beta * (a + c_values[0])) ** exponent_param) * (w_values[0] ** exponent_w)) / (a + c_values[0])
        common_public_good = q_[0]
    total_public_good = [(a * q) + (c * common_public_good) for c, q in zip(c_values, q_)]
    # welfare
    pi = [((w ** alpha) * (q_imp ** beta)) - q for c, w, q_imp, q in zip(c_values, w_values, total_public_good, q_)]
    sum_pi = sum(pi)
    return common_public_good, q_, sum_pi, pi


def main():
    # Parameters
    wealth = np.array([5000, 4500])
    beta = 0.4
    alpha = 0.4
    n = 2
    a = 5
    costs = np.array([3,5])

    # adding bounds for the maximization problem
    bounds = (0, None)
    bounds_q = (bounds, bounds)
    # increments
    initial_delta = 0.01  # Initial value of delta
    delta_increment = 0.01  # Fixed increment for delta
    num_deltas = 200  # Number of different delta values
    # the lists
    average_wealth = []
    average_cost = []
    iteration = []
    # welfare denoted by relative amounts for nash
    rw_good_contribution = []
    rw_good_nash_1 = []
    rw_good_nash_2 = []
    rw_welfare_1_nash = []
    rw_welfare_2_nash = []
    rw_sum_welfare_nash = []
    # heterogeneous welfare case
    rw_het_good_contribution = []
    rw_het_good_nash_1 = []
    rw_het_good_nash_2 = []
    rw_het_welfare_1_nash = []
    rw_het_welfare_2_nash = []
    rw_het_sum_welfare_nash = []
    # social planner
    rw_het_soc_optimum = []
    rw_het_sum_welfare_soc = []
    # welfare denoted by relative amounts for soc planner
    rw_soc_optimum = []
    rw_sum_welfare_soc = []

    # diff b/w nash and social optimum
    diff_soc_nash_hetero = []
    diff_soc_nash_homo = []

    for i in range(num_deltas):
        # Calculate delta based on the current iteration
        delta = initial_delta + (i * delta_increment)

        # Create a new distribution by adding delta to each income
        # new_distribution = wealth + delta
        new_distribution = wealth
        new_costs = [costs[0] - delta, costs[1] + delta]
        avg_cost = np.mean(new_costs)
        w_1 = new_distribution[0]
        w_2 = new_distribution[1]

        sum_wealth = w_1 + w_2
        w_relative = [v / sum_wealth for v in new_distribution]
        # Calculate the average income and append it to the list
        average_w = np.mean(new_distribution)
        # social planners optimization
        solution_relative = minimize(welfare_social_optimum_q(w_relative[0], w_relative[1], a, avg_cost, beta, alpha),
                                     (0, 0), method="trust-constr", bounds=bounds_q)
        solution_relative_het = minimize(
            welfare_social_optimum_het(w_relative[0], w_relative[1], a, new_costs, beta, alpha), (0, 0),
            method="trust-constr", bounds=bounds_q)

        rw_social_optimum = solution_relative.x
        f_max_relative = -solution_relative.fun
        rw_het_social_optimum = solution_relative_het.x
        f_max_relative_het = -solution_relative_het.fun

        # Calculate the amount of the public good of the distribution
        (rw_public_good_nash_homo, rw_individual_contribution_nash_homo, rw_profit_nash_homo,
         rw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(w_relative, beta, a, avg_cost, alpha, n)
        # for heterogeneous
        (rw_public_good_nash_hetero, rw_individual_contribution_nash_hetero, rw_profit_nash_hetero,
         rw_ind_profit_nash_hetero) = (
            nash_calculator_cobb_douglas_heterogeneous(w_relative, beta, a, new_costs, alpha, n))

        rw_soc_opt = sum(rw_social_optimum)
        rw_het_soc_opt = sum(rw_het_social_optimum)
        # diff soc nash
        diff_soc_nash_het = (f_max_relative_het - rw_profit_nash_hetero) / rw_profit_nash_hetero
        diff_soc_nash_ho = (f_max_relative - rw_profit_nash_homo) / rw_profit_nash_homo
        diff_absolute = f_max_relative - rw_profit_nash_homo
        rw_soc_optimum.append(rw_soc_opt)
        # Add the list of values to the plot
        average_wealth.append(average_w)
        average_cost.append(avg_cost)
        iteration.append(i)
        rw_sum_welfare_soc.append(f_max_relative)
        # relative wealth
        rw_good_contribution.append(rw_public_good_nash_homo)
        rw_welfare_1_nash.append(rw_ind_profit_nash_homo[0])
        rw_welfare_2_nash.append(rw_ind_profit_nash_homo[1])
        rw_good_nash_1.append(rw_individual_contribution_nash_homo[0])
        rw_good_nash_2.append(rw_individual_contribution_nash_homo[1])

        # small edit
        rw_sum_wel_nash = sum(rw_ind_profit_nash_homo)
        rw_sum_welfare_nash.append(rw_sum_wel_nash)
        # relative wealth; heterogeneous
        rw_het_good_contribution.append(rw_public_good_nash_hetero)
        rw_het_good_nash_1.append(rw_individual_contribution_nash_hetero[0])
        rw_het_good_nash_2.append(rw_individual_contribution_nash_hetero[1])
        rw_het_welfare_1_nash.append(rw_ind_profit_nash_hetero[0])
        rw_het_welfare_2_nash.append(rw_ind_profit_nash_hetero[1])
        rw_het_sum_welfare_nash.append(rw_profit_nash_hetero)
        rw_het_soc_optimum.append(rw_het_soc_opt)
        rw_het_sum_welfare_soc.append(f_max_relative_het)
        # welfare

        # rw_sum_welfare_nash.append(rw_profit_nash_homo)
        # (soc - nash)/nash
        diff_soc_nash_hetero.append(diff_soc_nash_het)
        diff_soc_nash_homo.append(diff_soc_nash_ho)

    # Plot the graph
    rcParams.update({'figure.autolayout': True})

    # Create subplots

    # Example 1
    # Plot the first subplot
    fig1, axs1 = plt.subplots(2,2)
    fig1.suptitle('Initial wealths: [5000, 4500]')

    axs1[0,0].plot(iteration, rw_good_contribution, label='Homogeneity', color='blue', marker='o')
    axs1[0,0].plot(iteration, rw_het_good_contribution, label='Heterogeneity', color='red', marker='o')
    axs1[0,0].set_title('Nash comparison: Public Good')
    axs1[0,0].set_xlabel('Iteration')
    axs1[0,0].set_ylabel('$Q^*$')
    axs1[0,0].legend(loc="lower right")

    axs1[0, 1].plot(iteration, rw_sum_welfare_nash, label='Homogeneity', color='blue', marker='o')
    axs1[0, 1].plot(iteration, rw_het_sum_welfare_nash, label='Heterogeneity', color='red', marker='o')
    axs1[0, 1].set_title('Nash comparison: Total Welfare')
    axs1[0, 1].set_xlabel('Iteration')
    axs1[0, 1].set_ylabel('Welfare')
    # axs1[0, 1].legend(loc="lower right")

    axs1[1, 0].plot(iteration, diff_soc_nash_homo, label='Homogeneity', color='blue', marker='o')
    axs1[1, 0].plot(iteration, diff_soc_nash_hetero, label=' Heterogeneity', color='red', marker='o')
    axs1[1, 0].set_title('(Soc Planner - Nash)/Nash')
    axs1[1, 0].set_xlabel('Iteration')
    axs1[1, 0].set_ylabel('Welfare')
    # axs1[1, 0].legend(loc="lower right")

    axs1[1,1].plot(iteration, rw_sum_welfare_soc, label='Homogeneity', color='blue', marker='o')
    axs1[1,1].plot(iteration, rw_het_sum_welfare_soc, label='Heterogeneity', color='red', marker='o')
    axs1[1,1].set_title('Social Planner comparison: Total Welfare')
    axs1[1,1].set_xlabel('Iteration')
    axs1[1,1].set_ylabel('$Welfare$')
    # axs1[1,1].legend(loc="lower right")

    fig2, axs2 = plt.subplots(2,2)
    fig2.suptitle('Initial wealths: [5000, 4500]')

    axs2[0,0].plot(iteration, rw_good_nash_1, label='Homogeneity', color='blue', marker='o')
    axs2[0,0].plot(iteration, rw_het_good_nash_1, label='Heterogeneity', color='red', marker='o')
    axs2[0,0].set_title('Country 1: Public Good')
    axs2[0,0].set_xlabel('Iteration')
    axs2[0,0].set_ylabel('$q_1^*$')
    axs2[0,0].legend(loc="lower right")

    axs2[0,1].plot(iteration, rw_welfare_1_nash, label='Homogeneity', color='blue', marker='o')
    axs2[0,1].plot(iteration, rw_het_welfare_1_nash , label='Heterogeneity', color='red', marker='o')
    axs2[0,1].set_title('Country 1: Welfare')
    axs2[0,1].set_xlabel('Iteration')
    axs2[0,1].set_ylabel('Welfare')

    axs2[1,0].plot(iteration, rw_good_nash_2, label='Homogeneity', color='blue', marker='o')
    axs2[1,0].plot(iteration, rw_het_good_nash_2, label=' Heterogeneity', color='red', marker='o')
    axs2[1,0].set_title('Country 2: Public Good')
    axs2[1,0].set_xlabel('Iteration')
    axs2[1,0].set_ylabel('$q_2^*$')
    #   axs2[1,0].legend(loc="lower right")

    axs2[1,1].plot(iteration, rw_welfare_2_nash, label='Homogeneity', color='blue', marker='o')
    axs2[1,1].plot(iteration, rw_het_welfare_2_nash, label='Heterogeneity', color='red', marker='o')
    axs2[1,1].set_title('Country 2: Welfare')
    axs2[1,1].set_xlabel('Iteration')
    axs2[1,1].set_ylabel('Welfare')

    # Adjust layout
    plt.tight_layout()

    # Add title
    # plt.title('Increasing wealth of all countries, alpha = 0.4, beta = 0.4')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()



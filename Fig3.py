# this Python file recreates Figure 3 of the paper.
import numpy as np
import matplotlib.pyplot as plt
from functionsFig3 import function_looper_endog,check_r_arrays
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator


# all functions are in the file functionsFig3


def main():
    #  start with an array of wealth
    wealth = np.array([5000, 500])
    # using functions to extract endogeneous power game and usual power game (absolute and relative)
    (aw_endogeneous_game_values, rw_endogeneous_game_values, aw_game_values, rw_game_values, r_values) = function_looper_endog(
        wealth)
    # this extraction gets us the arrays of how wealth increases, and the corresponding values of total public good with
    # soft power: rw_sum_public_good_endog
    # the levels of individual contributions at soft power: rw_good_nash_endo_1/2
    # similarly, welfare  at soft power equilibrium is rw_welfare_endog_nash_1/2 and sum
    (average_wealth, rw_sum_public_good_endog, rw_good_nash_endo_1, rw_good_nash_endo_2, rw_welfare_endog_nash_1,
     rw_welfare_endog_nash_2, rw_welfare_endog_sum) = rw_endogeneous_game_values
    #and the corresponding values under rival power:
    (rw_good_contribution, rw_good_nash_1, rw_good_nash_2, rw_welfare_1_nash, rw_welfare_2_nash,
     rw_sum_welfare_nash) = rw_game_values

    # we extract the levels of function (r1) at the endogenous game solution for every level of wealth
    (r1_1, r1_2) = r_values

    # we check if r1 is positive or negative

    check_r_arrays(r1_1,r1_2)

    # Plot the graph
    rcParams.update({'figure.autolayout': True})
    # Comparing the two models Public Good + Welfare - Relative wealth
    fig1, axs1 = plt.subplots(3, 2)
    fig1.suptitle('Nash public good - Relative Wealth with initial wealths: [4000, 3500]', fontsize=12)

    axs1[0, 0].plot(average_wealth, rw_sum_public_good_endog, label='Soft Power', color='black', marker='o')
    axs1[0, 0].set_title('Total Public Good - Soft Power')
    axs1[0, 0].set_xlabel('Average total group wealth')
    axs1[0, 0].set_ylabel('$Q^*$')
    axs1[0, 0].yaxis.set_major_locator(MaxNLocator(nbins=2))

    axs1[1, 0].plot(average_wealth, rw_good_nash_endo_1, label='Soft Power', color='red', marker='o')
    axs1[1, 0].set_title('Contribution of Country 1')
    # axs1[1, 0].set_xlabel('Average total group wealth')
    axs1[1, 0].set_ylabel('$q_1^*$')
    axs1[1, 0].yaxis.set_major_locator(MaxNLocator(nbins=2))

    axs1[2, 0].plot(average_wealth, rw_good_nash_endo_2, label='Soft Power', color='blue', marker='o')
    axs1[2, 0].set_title('Contribution of Country 2')
    # axs1[1, 0].set_xlabel('Average total group wealth')
    axs1[2, 0].set_ylabel('$q_2^*$')
    axs1[2,0].yaxis.set_major_locator(MaxNLocator(nbins=2))

    axs1[0, 1].plot(average_wealth, rw_good_contribution, label='Relative Wealth', color='black', marker='o')
    axs1[0, 1].set_title('Total Public Good - Rival Power')
    axs1[0, 1].set_xlabel('Average total group wealth')
    axs1[0, 1].set_ylabel('$Q^*$')

    axs1[1, 1].plot(average_wealth, rw_good_nash_1, label='Relative Wealth', color='red', marker='o')
    axs1[1, 1].set_title('Contribution of Country 1')
    # axs1[1, 1].set_xlabel('Average total group wealth')
    axs1[1, 1].set_ylabel('$q_1^*$')

    axs1[2, 1].plot(average_wealth, rw_good_nash_2, label='Relative Wealth', color='blue', marker='o')
    axs1[2, 1].set_title('Contribution of Country 2')
    # axs1[1, 1].set_xlabel('Average total group wealth')
    axs1[2, 1].set_ylabel('$q_2^*$')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()

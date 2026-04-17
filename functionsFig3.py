import numpy as np
from scipy.optimize import least_squares


# this function calculates the first-order conditions for the endogeneous power game
def nash_q(params):
    w1, w2, a, c, beta, alpha = params

    def br_1(q):
        q1, q2 = q
        # Ensure non-negative values
        if q1 < 0 or q2 < 0 or (q1 + q2) <= 0:
            return 1e10  # Large penalty

        public_good = (a * q1) + (c * (q1 + q2))
        exp_alpha = 1 - alpha
        exp_beta = 1 - beta

        term_1 = alpha * (1 / ((w1 + q1) ** exp_alpha)) * (public_good ** beta)
        term_2 = ((w1 + q1) ** alpha) * beta * (1 / (public_good ** exp_beta)) * (a + c)
        foc_1 = term_1 + term_2 - 1
        return foc_1

    def br_2(q):
        q1, q2 = q
        # Ensure non-negative values
        if q1 < 0 or q2 < 0 or (q1 + q2) <= 0:
            return 1e10  # Large penalty

        public_good = (a * q2) + c * (q1 + q2)
        exp_alpha = 1 - alpha
        exp_beta = 1 - beta

        term_1 = alpha * (1 / ((w2 + q2) ** exp_alpha)) * (public_good ** beta)
        term_2 = ((w2 + q2) ** alpha) * beta * (1 / (public_good ** exp_beta)) * (a + c)
        foc_2 = term_1 + term_2 - 1
        return foc_2

    def game(q):
        return [br_1(q), br_2(q)]

    return game

# calculates the first-order conditions for the endogeneous power game
def welfare_calculator_endog(q_1, q_2, w_1, w_2, a, c, alpha, beta):
    common_good = c * (q_1 + q_2)
    pi_1 = ((w_1 + q_1) ** alpha) * (((a * q_1) + common_good) ** beta)
    pi_2 = ((w_2 + q_2) ** alpha) * (((a * q_1) + common_good) ** beta)
    sum_pi = pi_1 + pi_2
    return sum_pi, pi_1, pi_2

# nash equilibrium calculator for absolute and relative wealth
def nash_calculator_cobb_douglas_homogeneous(w_values, beta, a, c, alpha, n):
    exponent_param = 1 / (1 - beta)
    exponent_w = alpha * exponent_param
    aggregation_g = sum(w ** (alpha / (1 - beta)) for w in w_values)
    # calculate public good
    common_public_good = (((beta * (a + c)) ** exponent_param) * aggregation_g) / (a + (c * n))
    # individual public good amounts
    q_ = (((beta * (a + c)) ** exponent_param) * (
            np.array(w_values) ** (alpha / (1 - beta))) - c * common_public_good) / a
    # allows for corner solutions
    if np.any(q_ < 0):
        q_[1] = 0
        q_[0] = (((beta * (a + c)) ** exponent_param) * ((w_values[0]) ** exponent_w)) / (a + c)
        common_public_good = q_[0]
    total_public_good = [(a * q + c * common_public_good) for q in q_]
    # welfare
    pi = (np.array(w_values) ** alpha) * ((np.array(total_public_good)) ** beta) - np.array(q_)
    sum_pi = sum(pi)
    return common_public_good, q_, sum_pi, pi



def r_1_calculator(q_1, q_2, w_1, w_2, a, c, alpha, beta):
    y = {
        1: w_1 + q_1,
        2: w_2 + q_2
    }
    z = {
        1: a * q_1 + c * (q_1 + q_2),
        2: a * q_2 + c * (q_1 + q_2)
    }

    # Initialize dictionaries to hold our results
    Byy = {}
    Bzz = {}
    Byz = {}
    r = {}
    # Loop through both agents to calculate derivatives and r simultaneously
    for i in [1, 2]:
        Byy[i] = alpha * (alpha - 1) * (y[i] ** (alpha - 2)) * (z[i] ** beta)
        Bzz[i] = beta * (beta - 1) * (y[i] ** alpha) * (z[i] ** (beta - 2))
        Byz[i] = alpha * beta * (y[i] ** (alpha - 1)) * (z[i] ** (beta - 1))

        # Calculate r_i for the current agent
        numerator = -(Byy[i] + Byz[i] * (a + c))
        denominator = (Byy[i] + Byz[i] * (a + c) ) + a * (Byz[i] + Bzz[i] * (a + c))

        r[i] = numerator / denominator
    # Return a comprehensive dictionary with all computed values
    return r[1], r[2]


def check_r_arrays(r1, r2):
    # Check conditions for r1
    if all(x > 0 for x in r1):
        print("all r1 positive")
    elif all(x < 0 for x in r1):
        print("all r1 neg")
    else:
        print("r1 is mixed or contains zeros. Array:")
        print(r1)

    # Check conditions for r2
    if all(x > 0 for x in r2):
        print("all r2 positive")
    elif all(x < 0 for x in r2):
        print("all r2 neg")
    else:
        print("r2 is mixed or contains zeros. Array:")
        print(r2)


# loops over increments in wealth and calculates levels of public good and welfare
def function_looper_endog(wealth):
    # Parameters
    alpha = 0.4
    beta = 0.4
    c = 1
    a = 1
    n = 2
    # increments
    initial_delta = 5  # Initial value of delta
    delta_increment = 5  # Fixed increment for delta
    num_deltas = 200  # Number of different delta values


    # arrays holding the PG amounts/welfare over iterations
    average_wealth = []
    aw_sum_public_good_endog = []
    aw_good_nash_endo_1 = []
    aw_good_nash_endo_2 = []
    aw_welfare_endog_nash_1 = []
    aw_welfare_endog_nash_2 = []
    aw_welfare_endog_sum = []

    rw_sum_public_good_endog = []
    rw_good_nash_endo_1 = []
    rw_good_nash_endo_2 = []
    rw_welfare_endog_nash_1 = []
    rw_welfare_endog_nash_2 = []
    rw_welfare_endog_sum = []

    aw_good_contribution = []
    aw_good_nash_1 = []
    aw_good_nash_2 = []
    aw_welfare_1_nash = []
    aw_welfare_2_nash = []
    aw_sum_welfare_nash = []
    # welfare denoted by relative amounts for nash
    rw_good_contribution = []
    rw_good_nash_1 = []
    rw_good_nash_2 = []
    rw_welfare_1_nash = []
    rw_welfare_2_nash = []
    rw_sum_welfare_nash = []

    # r_1 for countries 1 and 2
    r1_1 = []
    r1_2 = []

    # iterations
    for i in range(num_deltas):
        # Calculate delta based on the current iteration
        delta = initial_delta + (i * delta_increment)

        # Create a new distribution by adding delta to each income
        new_distribution = wealth + delta

        w_1 = new_distribution[0]
        w_2 = new_distribution[1]

        sum_wealth = w_1 + w_2
        w_relative = [v / sum_wealth for v in new_distribution]

        # Calculate the average income and append it to the list
        average = np.mean(new_distribution)

        # Add the list of values to the plot
        average_wealth.append(average)
        params_1 = w_1, w_2, a, c, beta, alpha
        params_2 = w_relative[0], w_relative[1], a, c, beta, alpha
        # Use least_squares with bounds instead of fsolve
        game_1 = nash_q(params_1)
        game_2 = nash_q(params_2)
        # Bounds: both q1 and q2 must be >= 0
        result_game_1 = least_squares(
            lambda q: game_1(q),
            x0=[100, 100],  # Initial guess
            bounds=([0, 0], [np.inf, np.inf])  # q1, q2 >= 0
        )

        result_game_2 = least_squares(
            lambda q: game_2(q),
            x0=[100, 100],  # Initial guess
            bounds=([0, 0], [np.inf, np.inf])  # q1, q2 >= 0
        )
        # calculate nash for standard model
        (aw_public_good_nash_homo, aw_individual_contribution_nash_homo, aw_profit_nash_homo,
         aw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(new_distribution, beta, a, c, alpha, n)
        (rw_public_good_nash_homo, rw_individual_contribution_nash_homo, rw_profit_nash_homo,
         rw_ind_profit_nash_homo) = nash_calculator_cobb_douglas_homogeneous(w_relative, beta, a, c, alpha, n)

        answers_game1_endo = result_game_1.x
        answers_game2_endo = result_game_2.x

        aw_sum_public_good = answers_game1_endo[0] + answers_game1_endo[1]
        rw_sum_public_good = answers_game2_endo[0] + answers_game2_endo[1]
        print(rw_sum_public_good)
        # calculate welfare for endogeneous wealth
        (welfare_endog_game1_total, welfare_endog_game1_1, welfare_endog_game1_2) = welfare_calculator_endog(
            answers_game1_endo[0], answers_game1_endo[1], w_1, w_2, a, c, alpha, beta)
        (welfare_endog_game2_total, welfare_endog_game2_1, welfare_endog_game2_2) = welfare_calculator_endog(
            answers_game2_endo[0], answers_game2_endo[1], w_relative[0], w_relative[1], a, c, alpha, beta)

        (r_1, r_2) = r_1_calculator(answers_game2_endo[0], answers_game2_endo[1], w_relative[0], w_relative[1], a, c,
                                    alpha, beta)

        # appending values from the iterations : endogeneous power model - absolute
        aw_good_nash_endo_1.append(answers_game1_endo[0])
        aw_good_nash_endo_2.append(answers_game2_endo[1])
        aw_sum_public_good_endog.append(aw_sum_public_good)
        aw_welfare_endog_nash_1.append(welfare_endog_game1_1)
        aw_welfare_endog_nash_2.append(welfare_endog_game1_2)
        aw_welfare_endog_sum.append(welfare_endog_game1_total)

        # relative
        rw_good_nash_endo_1.append(answers_game2_endo[0])
        rw_good_nash_endo_2.append(answers_game2_endo[1])
        rw_sum_public_good_endog.append(rw_sum_public_good)
        rw_welfare_endog_nash_1.append(welfare_endog_game2_1)
        rw_welfare_endog_nash_2.append(welfare_endog_game2_2)
        rw_welfare_endog_sum.append(welfare_endog_game2_total)

        # absolute wealth - nash
        aw_good_contribution.append(aw_public_good_nash_homo)
        aw_good_nash_1.append(aw_individual_contribution_nash_homo[0])
        aw_good_nash_2.append(aw_individual_contribution_nash_homo[1])
        aw_welfare_1_nash.append(aw_ind_profit_nash_homo[0])
        aw_welfare_2_nash.append(aw_ind_profit_nash_homo[1])
        aw_sum_welf = sum(aw_ind_profit_nash_homo)
        aw_sum_welfare_nash.append(aw_sum_welf)
        # relative wealth
        rw_good_contribution.append(rw_public_good_nash_homo)
        rw_welfare_1_nash.append(rw_ind_profit_nash_homo[0])
        rw_welfare_2_nash.append(rw_ind_profit_nash_homo[1])
        rw_good_nash_1.append(rw_individual_contribution_nash_homo[0])
        rw_good_nash_2.append(rw_individual_contribution_nash_homo[1])
        # small edit
        rw_sum_welf = sum(rw_ind_profit_nash_homo)
        rw_sum_welfare_nash.append(rw_sum_welf)

        # r_1
        r1_1.append(r_1)
        r1_2.append(r_2)

    aw_endogeneous_game_values = (average_wealth, aw_sum_public_good_endog, aw_good_nash_endo_1, aw_good_nash_endo_2,
                                  aw_welfare_endog_nash_1, aw_welfare_endog_nash_2, aw_welfare_endog_sum)
    rw_endogeneous_game_values = (average_wealth, rw_sum_public_good_endog, rw_good_nash_endo_1, rw_good_nash_endo_2,
                                  rw_welfare_endog_nash_1, rw_welfare_endog_nash_2, rw_welfare_endog_sum)
    aw_game_values = (aw_good_contribution, aw_good_nash_1, aw_good_nash_2, aw_welfare_1_nash, aw_welfare_2_nash,
                      aw_sum_welfare_nash)
    rw_game_values = (rw_good_contribution, rw_good_nash_1, rw_good_nash_2, rw_welfare_1_nash, rw_welfare_2_nash,
                      rw_sum_welfare_nash)
    r_values = (r1_1, r1_2)

    return aw_endogeneous_game_values, rw_endogeneous_game_values, aw_game_values, rw_game_values, r_values

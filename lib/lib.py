import math as m

'''
Aircraft configuration class
'''


class Aircraft:
    def __init__(self):
        self.n_pax = 120
        self.w_pax = 80
        self.w_bags = 20
        self.n_crew = 5
        self.w_crew = (self.n_crew * self.w_pax)
        self.w_cargo = (self.n_pax * self.w_bags)
        self.w_payload = (self.n_pax * self.w_pax) + self.w_cargo  # Weight of pax and baggage
        self.cruise_mach = 0.75
        self.w_climb_frac = float(1.0065 - 0.0325 * self.cruise_mach)
        self.range = 5000000
        self.loiter = 45 * 60
        self.cruise_alt = 8000
        self.v_cruise = 308.1 * self.cruise_mach
        self.l_to_d_max = 20
        self.l_to_d_cruise = 0.866 * self.l_to_d_max
        self.sfc_cruise = 0.5 / 3600
        self.wetted_area_ratio = 2.4
        self.sfc_loiter = 0.4 / 3600

    """ Take-off Gross weight """

    def togw(self):

        A = 1.02
        C = -0.06

        w_warmup_frac = 0.97
        w_taxi_frac = 0.97
        w_takeoff_frac = 0.97
        w_desc_frac = 1
        w_landing_frac = 0.995

        """ Cruise Estimation """

        exp_cruise = (-self.range * self.sfc_cruise) / (self.v_cruise * self.l_to_d_cruise)
        w_cruise_frac = m.exp(exp_cruise)

        """ Loiter Estimation """

        exp_loiter = (-(self.loiter * self.sfc_loiter) / self.l_to_d_max)
        w_loiter_frac = m.exp(exp_loiter)

        total_w_frac = w_warmup_frac * w_taxi_frac * w_takeoff_frac * self.w_climb_frac * w_cruise_frac * w_loiter_frac * w_desc_frac * w_landing_frac

        """ Estimation of mission fuel fraction"""
        w_fuel_frac = (1 + 0.05) * (1 - total_w_frac)

        """ Variable sweep constant """

        # TODO: check sweep type - if 'f_sweep' else 1.04
        K_vs = 1.0

        guess = round((6 * (self.w_crew + self.w_payload)), 4)

        i = 100
        while i < 101:
            w_empty_fraction = round(A * m.pow(guess, C) * K_vs, 4)

            denominator = (1 - w_empty_fraction - w_fuel_frac)
            gross = round(((self.w_payload + self.w_crew) / denominator), 4)

            e = (guess - gross) / 100

            print('LHS ||   ' + str(guess), '', 'w_empty_frac ||   ' + str(w_empty_fraction), '', 'RHS ||   ', gross,
                  ' ', 'e ||  ' + str(e))

            guess += round(gross, 4)
            guess /= 2
            if round(e, 2) < 0.02:
                print(round(gross, 2))
                props = {
                    'w_0': round(gross, 2),
                    'w_f': round((gross * w_fuel_frac), 4),
                    'w_e': round((gross * w_empty_fraction), 4)
                }
                print(props)
                return round(gross, 2)
            else:
                pass

        # Wetted aspect ratio

    def wetted_aspect_ratio(self, ar):
        """
        :param ar: aspect ratio
        :return: wetted aspect ratio

        """
        result = ar / self.wetted_area_ratio

        return result

a = Aircraft()

a.togw()
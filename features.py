import numpy as np
import math
from pyts.approximation import SymbolicAggregateApproximation
from scipy.stats import zscore


class RFeatures(object):
    def __init__(self, rspace_win, rspace_upper_bound, rspace_lower_bound, rspace_max_thresh=100):
        self.rspace_win = rspace_win
        self.rspace_max_thresh = rspace_max_thresh
        self.rspace_upper_bound = rspace_upper_bound
        self.rspace_lower_bound = rspace_lower_bound

    def r_detect(self, data: list) -> list:
        r_data = []
        for i in range(self.rspace_win, len(data) - self.rspace_win):
            current_window_mean = np.mean(data[i: i + self.rspace_win])
            before_window_mean = np.mean(data[i - self.rspace_win])
            if math.isclose(before_window_mean, 0.0):
                r_data.append(self.rspace_max_thresh)
            else:
                r_data.append(current_window_mean / before_window_mean)
        return r_data

    def judge_change_by_r(self, number: int) -> int:
        if number > self.rspace_upper_bound:
            return 1
        elif number <= self.rspace_lower_bound:
            return -1
        return 0

    def get_rTrans_result(self, data: list) -> list:
        r_data = self.r_detect(data)
        binary_sequence = [self.judge_change_by_r(elem) for elem in r_data]
        return binary_sequence

    def get_rSegments(self, data: list) -> np.array:
        binary_result = self.get_rTrans_result(data)

        segment = False
        threshold = 0
        start = []
        end = []
        for i in range(len(binary_result)):
            if binary_result[i] == 1 and segment is False:
                segment = True
                threshold = data[i + self.rspace_win]
                start.append(i + self.rspace_win)
                if i + 3 * self.rspace_win > len(data) - 1:
                    end.append(len(data) - 1)
                else:
                    end.append(i + 3 * self.rspace_win)
            if data[i + self.rspace_win] < threshold and segment is True:
                segment = False
                # end.append(i + self.rspace_win)
        if len(start) > len(end):
            end.append(len(data) + self.rspace_win)

        return np.concatenate((np.array(start).reshape(-1, 1), np.array(end).reshape(-1, 1)), axis=1)


class SAXFeatures(object):
    def __init__(self, bins: int):
        self.bins = bins

    def sax_transform(self, data: list):
        data = np.array(data).reshape(-1, 1)
        data = zscore(data)  # 要先Z score归一化
        data[np.isnan(data)] = 0.01
        sax = SymbolicAggregateApproximation(n_bins=self.bins, strategy='normal')
        x_sax = sax.fit_transform(data)

        return x_sax

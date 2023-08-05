import numpy as np
import cmath

class TimeSeries:
    """Stores data from different simulation sources.
    A TimeSeries object always consists of timestamps and datapoints.
    """
    def __init__(self, name, time, values, label=""):
        self.time = np.array(time)
        self.values = np.array(values)
        self.name = name
        self.label = name

    def scale(self, name, factor):
        """Returns scaled timeseries.
        Assumes the same time steps for both timeseries.
        """
        ts_scaled = TimeSeries(name, self.time, self.values * factor)
        return ts_scaled

    def abs(self, name):
        """ Calculate absolute value of complex time series.
        """
        abs_values = []
        for value in self.values:
            abs_values.append(np.abs(value))
        ts_abs = TimeSeries(name, self.time, abs_values)
        return ts_abs

    def phase(self, name):
        """ Calculate absolute value of complex time series.
        """
        phase_values = []
        for value in self.values:
            phase_values.append(np.angle(value, deg=True))
        ts_abs = TimeSeries(name, self.time, phase_values)
        ts_phase = TimeSeries(name, self.time, phase_values)
        return ts_phase

    def phasor(self, name):
        """Calculate phasor of complex time series and return dict with abs and phase.
        """
        ts_abs = self.abs(self.name + '_abs')
        ts_phase = self.phase(self.name + '_phase')
        ts_phasor = {}
        ts_phasor['abs'] = ts_abs
        ts_phasor['phase'] = ts_phase
        
        return ts_phasor

    @staticmethod
    def frequency_shift_list(timeseries_list, freq):
        """Calculate shifted frequency results of all time series
        :param timeseries_list: timeseries list retrieved from dpsim results
        :param freq: frequency by which the timeseries should be shifted
        :return: list of shifted time series
        """
        result_list = {}
        for name, ts in timeseries_list.items():
            ts_emt = ts.frequency_shift(ts.name, freq)
            result_list[ts.name] = ts_emt

        return result_list

    @staticmethod
    def rmse(ts1, ts2):
        """ Calculate root mean square error between two time series
        """
        return np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())

    @staticmethod
    def norm_rmse(ts1, ts2):
        """ Calculate root mean square error between two time series,
        normalized using the mean value of both mean values of ts1 and ts2 
        """
        if np.mean(np.array(ts1.values.mean(),ts2.values.mean())) != 0:
          nrmse = np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())/np.mean(np.array(ts1.values.mean(),ts2.values.mean()))
          is_norm = True
        else:
          nrmse = np.sqrt((TimeSeries.diff('diff', ts1, ts2).values ** 2).mean())
          is_norm = False
        return (nrmse,is_norm)

    @staticmethod
    def diff(name, ts1, ts2):
        """Returns difference between values of two Timeseries objects.
        """
        if len(ts1.time) == len(ts2.time):
            ts_diff = TimeSeries(name, ts1.time, (ts1.values - ts2.values))
        else:  # different timestamps, common time vector and interpolation required before substraction
            time = sorted(set(list(ts1.time) + list(ts2.time)))
            interp_vals_ts1 = np.interp(time, ts1.time, ts1.values)
            interp_vals_ts2 = np.interp(time, ts2.time, ts2.values)
            ts_diff = TimeSeries(name, time, (interp_vals_ts2 - interp_vals_ts1))
        return ts_diff

    def frequency_shift(self, name, freq):
        """ Shift dynamic phasor values to EMT by frequency freq.
            Assumes the same time steps for both timeseries.
        :param name: name of returned time series
        :param freq: shift frequency
        :return: new timeseries with shifted time domain values
        """
        ts_shift = TimeSeries(name, self.time, self.values.real*np.cos(2*np.pi*freq*self.time)
                              - self.values.imag*np.sin(2*np.pi*freq*self.time))
        return ts_shift

    def calc_freq_spectrum(self):
        """ Calculates frequency spectrum of the time series using FFT
        :param name: name of returned time series
        :param freq: shift frequency
        :return: new timeseries with shifted time domain values
        """
        Ts = self.time[1]-self.time[0]
        fft_values = np.fft.fft(self.values)
        freqs_num = int(len(fft_values)/2)
        fft_freqs = np.fft.fftfreq(len(fft_values),d=Ts)
        return fft_freqs[:freqs_num], np.abs(fft_values[:freqs_num])/freqs_num

    def interpolate_cmpl(self, name, timestep):
        """ Not tested yet!
        Interpolates complex timeseries with timestep
        :param name:
        :param timestep:
        :return:
        """
        interpl_time = np.arange(self.time[0], self.time[-1], timestep)
        realValues = interp1d(interpl_time, self.values.real)
        imagValues = interp1d(interpl_time, self.values.imag)
        ts_return = TimeSeries(name, time, np.vectorize(complex)(realValues, imagValues))
        return timeseries
    
    @staticmethod
    def check_node_number_comp(ts_list_comp, node):
        """
        Check if node number is available in complex time series.
        :param ts_comp: complex time series list
        :param node: node number to be checked
        :return: true if node number is available, false if out of range
        """
        ts_comp_length = len(ts_comp)
        im_offset = int(ts_comp_length / 2)
        if im_offset <= node or node < 0:
            print('Complex node not available')
            return false
        else:
            return true

    @staticmethod
    def check_node_number(ts_list, node):
        """
        Check if node number is available in time series.
        :param ts: time series list
        :param node: node number to be checked
        :return: true if node number is available, false if out of range
        """
        ts_length = len(ts)
        if ts_length <= node or node < 0:
            print('Node not available')
            return false
        else:
            return true

    @staticmethod
    def complex_abs(name, ts_real, ts_imag):
        """ Calculate absolute value of complex variable.
        Assumes the same time steps for both timeseries.
        """
        ts_complex = np.vectorize(complex)(ts_real.values, ts_imag.values)
        ts_abs = TimeSeries(name, ts_real.time, np.absolute(ts_complex))
        return ts_abs

    @staticmethod
    def phasors(timeseries_list):
        """Calculate voltage phasors of all nodes
        :param timeseries_list: timeseries list with real and imaginary parts
        :return: timeseries list with abs and phase
        """
        phasor_list = {}
        for name, ts in timeseries_list.items():
            phasor_list[name] = ts.phasor(name)

        return phasor_list
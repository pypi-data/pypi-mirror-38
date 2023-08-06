"""staging.py

The purpose of this script is allow one to automatically classify intracranial eeg data as either wake, Non-REM,
or not Non-REM. The way we calculate the stage is through the use of a metric called Visualization Index (VI).

Steps:
Window data into 30s epochs with 0s of overlap
Run a FFT over each 30s epoch
Normalize the resulting PSD across time and channels to 1 using the total area under the power spectrum.
Across subjects: normalize the scale so maximal VI value, for each channel, is equal to 100 and minimum is 1
Average all channels

Definitions:
                        delta = (1,4)
                        theta = (4, 8)
                        alpha = (8, 12)
                        spindle = (11,16)
                        high_beta = (20, 40)
                        VI = (delta + theta + spindle) / (high_beta, alpha)
"""
import numpy as np
from cmlreaders import CMLReader
from Clumsy import get_sub_tal
#from .io import get_sub_tal
from glob import glob
import os
from ptsa.data.filters import MonopolarToBipolarMapper
from IPython.display import display
from Clumsy import psd, rolling_window_full, TimeSeriesLF
from .data_organization import get_data_roots, get_subj_exp_sess_date_matcher
SUBJ_EXP_SESS_DATE_MATCHER = get_subj_exp_sess_date_matcher()
DATA_ROOTS = get_data_roots()

__all__ = ['VigilanceIndexPipeline']

# TODO: add more helpful warnings in, e.g. instead of keyerror from SUBJ_EXP do session not valid, if no paths exist print that.
class Error(BaseException):
    """Base class for exceptions in this module."""
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)

class DoneGoofed(Error):
    """Exception raised when no paths are found
    """
    def __init__(self, warning='', *args, **kwargs):
        Error.__init__(self, warning)

class DoneGoofed_InvalidSession(Error):
    """Exception raised for errors in the input, here if they didn't enter a valid session.
    Attributes:
        session -- input session of thes
        possible_sessions -- valid sessions of the subject
    """

    def __init__(self, session, possible_sessions):
        warning = 'DoneGoofed Session Error: Ah Shucks sorry to say but it looks someone done goofed...'
        warning2 = 'I could not find session {}. Have you considered using a valid session instead? Try: \n'
        self.warning = warning2.format(session)
        print(warning)
        print(self.warning)
        display(possible_sessions)

class VigilanceIndexPipeline(object):
    """Calculates the Vigilance index, a measure of depth of NREM _sleep

    Parameters
    ----------
    subject: str,
             subject ID, e.g. 'R1293P'
    experiment: str,
                experiment analyze
    session: str/int,
             behavioral session to analyze
    montage: str, by default 'bipolar',
             montage scheme to apply,
             valid: 'bipolar', 'bi', 'bp', 'pairs', 'monopolar', 'mono', 'mp', 'contacts'
    window_len: int, by default 30,
                length in seconds of window to calculate index over
    overlap: int, by default 0,
             length in seconds to allow overlap of windows when calculating index
    number_lat_chs: int, by default 10,
                    number of channels to include sorted by lateralization in the brain
    night_start_time: str, by default '2200',
                      time in 2400 to consider a night to start at, used in night before calculations
    morning_start_time: str, by default '0800',
                        time in 2400 to consider a morning to began at, used for night after calculations

    Notes
    -------
    The power spectrum density is normalized so that the total area under the curve is 1, afterwards this value must be
    normalized between 1-100 if comparing across subjects. By default this object will conduct both normalizations

    The purpose of this object is allow one to automatically classify intracranial eeg data as either Non-REM,
    or not Non-REM. The way we calculate the stage is through the use of a metric called Visualization Index (VI).

    Steps:
    Window data into 30s epochs with 0s of overlap
    Run a FFT over each 30s epoch
    Normalize the resulting PSD across time and channels to 1 using the total area under the power spectrum.
    Across subjects: normalize the scale so maximal VI value, for each channel, is equal to 100 and minimum is 1
    Average all channels

    Definitions:
                            delta = (1,4)
                            theta = (4, 8)
                            alpha = (8, 12)
                            spindle = (11,16)
                            high_beta = (20, 40)
                            VI = (delta + theta + spindle) / (high_beta, alpha)


    """
    VI_frequency_bands = {
        'delta' : (1, 4),
        'theta' :(4, 8),
        'alpha' : (8, 12),
        'spindle' : (11, 16),
        'high_beta' : (20, 40),
    }
    delta = (1, 4)
    theta = (4, 8)
    alpha = (8, 12)
    spindle = (11, 16)
    high_beta = (20, 40)
    VI = '(delta + theta + spindle) / (high_beta, alpha)'

    hpc_labels = np.array(['Left CA1', 'Left CA2', 'Left CA3', 'Left DG', 'Left Sub',
                           'Right CA1', 'Right CA2', 'Right CA3', 'Right DG', 'Right Sub'])
    mtl_labels = np.append(hpc_labels, np.array(['Left PRC', 'Left EC', 'Right PRC', 'Right EC']))
    downsampled_root = '/data/eeg/LFSleep/ProcData/{}/**/*100hz.h5'
    fmt = "%m_%d_%y_%H%M" # month, day, year (decimal format, e.g. 18 not 2018), hour in 2400, minute

    def __init__(self, subject, experiment, session, montage='bipolar', window_len=30, overlap=0, number_lat_chs=10,
                 night_before=True, night_start_time='2200', morning_start_time='0800'):
        """Calculates the Vigilance index, a measure of depth of NREM _sleep
           Where:
           delta = (1, 4)
           theta = (4, 8)
           alpha = (8, 12)
           spindle = (11, 16)
           high_beta = (20, 40)
           VI = (delta + theta + spindle) / (high_beta, alpha)


        Parameters
        ----------
        subject: str,
                 subject ID, e.g. 'R1293P'
        experiment: str,
                    experiment analyze
        session: str/int,
                 behavioral session to analyze
        montage: str, by default 'bipolar',
                 montage scheme to apply,
                 valid: 'bipolar', 'bi', 'bp', 'pairs', 'monopolar', 'mono', 'mp', 'contacts'
        window_len: int, by default 30,
                    length in seconds of window to calculate index over
        overlap: int, by default 0,
                 length in seconds to allow overlap of windows when calculating index
        number_lat_chs: int, by default 10,
                        number of channels to include sorted by lateralization in the brain
        night_before: bool, by default True,
                      whether to look at the night before (True) or after (False) the experiment
        night_start_time: str, by default '2200',
                          time in 2400 to consider a night to start at, used in night before calculations
        morning_start_time: str, by default '0800',
                            time in 2400 to consider a morning to began at, used for night after calculations
        """
        self.subject = subject
        self.experiment = experiment
        self.session = session
        self.montage = montage
        self.window_len = window_len # In seconds
        self.overlap = overlap # In seconds
        self.n = number_lat_chs # Calculate using n most lateral channels
        self.night_before = night_before
        self.night_start_time = night_start_time
        self.morning_start_time = morning_start_time

        self.mp, self.bp, self.tal = get_sub_tal(subject, experiment, True)
        self.reader = CMLReader(subject=self.subject,
                                experiment=self.experiment,
                                session=self.session)
        self.pairs = self.reader.load('pairs')
        self.contacts = self.reader.load('contacts')
        self.electrode_categories = self.reader.load('electrode_categories')
        self.epileptic_channels = np.unique(np.concatenate((self.electrode_categories['soz'],
                                                            self.electrode_categories['interictal'])))

        if self.montage in ('bipolar', 'bi', 'bp', 'pairs'):
            self.channels_df = self.pairs
            self.montage = 'bipolar'
        elif self.montage in ('monopolar', 'mono', 'mp', 'contacts'):
            self.channels_df = self.contacts
            self.montage = 'monopolar'
        else:
            raise ValueError(
                'Expected either "monopolar" or "bipolar" as montage input but got {}'.format(self.montage))

        self.sleep_paths = glob(VigilanceIndexPipeline.downsampled_root.format(self.subject), recursive=True)
        try:
            self.experimental_date = SUBJ_EXP_SESS_DATE_MATCHER[self.subject.upper(
            )][self.experiment.lower()][str(self.session)]
        except KeyError: # If session is invalid
            df = CMLReader.get_data_index()
            df = df[df['subject'] == self.subject]
            DoneGoofed_InvalidSession(session=self.session, possible_sessions=df[['experiment', 'session']].T)

        self.load_data_paths = self.get_sleep_recording_paths()

        return

    def run_detection(self):
        """Main function to call to run the pipeline

        Returns
        -------
        Vigilance Index, normalized between values of 0-100 where higher numbers indicate deeper _sleep
        """
        ts = self.fft_from_whole_night()

        # Normalize by area under the curve (values sum to 1)
        ts = self._normalize_by_integral(ts)
        #ts = self.average_frequencies_into_bands(ts)

        ts = self.frequencies_into_bands(ts, how = 'sum')
        VI = (ts.sel(frequency='delta') + ts.sel(frequency='theta') + ts.sel(frequency='spindle')
             ) / (ts.sel(frequency='alpha') + ts.sel(frequency='high_beta'))
        return self._normalize_zero_to_high(VI.mean('channels'))


    def sort_channels_by_lateralization(self):
        """Returns an array of the most lateral channels in the subject

        Returns
        -------
        channels_sorted_laterally: np.array, indices corresponding to the sorted channels
        """
        absolute_lateral = np.abs(np.array(self.channels_df['ind.x']))  # np.abs ensures handling left/right the same
        channels_sorted_laterally = np.argsort(absolute_lateral)[::-1]
        return channels_sorted_laterally

    def get_n_most_lateral_channel_indices(self, n=None):
        """Return indices corresponding to n most lateral channels

        Parameters
        ----------
        n: int, by default None
           the number of channels to include, only change this when it's desirable to not use the instance's attribute

        Returns
        -------
        lateral_channel_indices: np.array, indices corresponding to the desired channels
        """
        if n is None:
            n = self.n

        if self.montage == 'monopolar':
            # Get n most lateral contacts that are not epileptic
            keep = ~np.isin(self.sort_channels_by_lateralization(),
                            np.where(np.isin(self.channels_df['label'], self.epileptic_channels))[0])
            lateral_channel_indices = self.sort_channels_by_lateralization()[keep][:n]
            return lateral_channel_indices

        elif self.montage == 'bipolar':
            ch0= np.array(list(map(lambda s:s.split('-')[0], self.channels_df['label'])))
            ch1 = np.array(list(map(lambda s:s.split('-')[1], self.channels_df['label'])))
            keep0 = ~np.isin(self.sort_channels_by_lateralization(),
                             np.where(np.isin(ch0, self.epileptic_channels))[0])
            keep1 = ~np.isin(self.sort_channels_by_lateralization(),
                             np.where(np.isin(ch1, self.epileptic_channels))[0])
            lateral_channel_indices = self.sort_channels_by_lateralization()[keep0 & keep1][:n]
            return lateral_channel_indices

    def filter_lateral_channels(self, timeseries):
        """Fetch relevant lateral channels and filters the data using montage scheme

        Parameters
        ----------
        timeseries: TimeSeriesLF, MONOPOLAR timeseries to filter

        Returns
        -------
        timeseries: TimeSeriesLF, timeseries containing only the lateral channels, either as monopolar referrenced or
        bipolar referenced depending on self.montage
        """
        relevant_channels = self.get_n_most_lateral_channel_indices()
        # Make sure we only pick valid channels
        timeseries = timeseries.sel(channels=np.isin(timeseries.channels, self.contacts['label']))
        if self.montage == 'monopolar':
            timeseries = timeseries[relevant_channels]

        # Need to re-reference from monopolar data in the path
        elif self.montage == 'bipolar':
            valid_mp = np.unique(np.concatenate((self.bp['ch0'][relevant_channels],
                                                 self.bp['ch1'][relevant_channels])))
            valid_bp = self.bp[relevant_channels]
            timeseries['channels'].data = self.mp
            timeseries = timeseries.sel(channels=valid_mp)
            mono2bi = MonopolarToBipolarMapper(timeseries, bipolar_pairs=valid_bp)
            timeseries = mono2bi.filter()
        return timeseries

    def get_sleep_recording_paths(self):
        """Return an array of paths for all valid 100hz resampled data for a given session's previous night or
        subsequent night

        Returns
        -------
        path_files: np.array, array of valid paths from the night before the relevant session
        """
        # Path formatting is month_day_year_start_stop, e.g. '8_12_11_0320_0450... .h5'
        dates_formatted = ['_'.join(x.split('_')[:4]) for x in
                           list(map(os.path.basename, self.sleep_paths))]

        # Date the experiment took place and relevant datetime string formatting
        start_date_formatted = '_'.join(self.experimental_date.split('_')[:4])
        month, day, year, hour_minutes = start_date_formatted.split('_')
        night_before_start_date_formatted = '_'.join([month, str(int(day) - 1), year, self.night_start_time])
        morning_after_start_date_formatted = '_'.join([month, str(int(day) + 1), year, self.morning_start_time])

        # Go through all paths subject has on rhino and pull any that match signature pattern
        path_files = []
        for i, date_path in enumerate(dates_formatted):

            if self.night_before:
                if (date_path < start_date_formatted) and (date_path > night_before_start_date_formatted):
                    path_files.append(self.sleep_paths[i])

            elif not self.night_before:
                if (date_path > start_date_formatted) and (date_path < morning_after_start_date_formatted):
                    path_files.append(self.sleep_paths[i])
        if len(path_files) == 0:
            raise DoneGoofed('No paths found, ensure that the data are properly uploaded to rhino in the format requested')
        return sorted(np.array(path_files))


    def load_whole_night_rolled_intervals(self):
        """Load the entire night's downsampled data, chunking into self.window_len long intervals

        Returns
        -------
        rolled_data: np.array, data rolled into 30s chunks concatenated across paths/epochs
        """
        # Create rolling windows to compute power spectral density over
        rolling = []
        for path in self.load_data_paths:
            dat = TimeSeriesLF.from_hdf(path)
            dat = self.filter_lateral_channels(dat)

            step = dat._TimeSeries__duration_to_samples(self.window_len)
            asteps = dat._TimeSeries__duration_to_samples(self.window_len - self.overlap)
            arr = dat.data
            rolled = rolling_window_full(array=arr, window=step, asteps=asteps)
            rolling.append(rolled.transpose(1, 0, 2)) # Transpose so we can concat over paths/epochs
        try:
            rolled_data = np.concatenate(rolling).transpose(1, 0, 2)
        except ValueError as e:
            # If there aren't any files
            print(e)

        return rolled_data

    def fft_from_whole_night(self):
        """Calculates rolling Fast Fourier Transformation using Welch's mean method


        Returns
        -------
        ts: TimeSeriesLF,
            time series data of power spectrum density across a whole night's recording
        """
        # Create rolling windows to compute power spectral density over
        rolled_data = self.load_whole_night_rolled_intervals()
        channels = self.channels_df['label'][self.get_n_most_lateral_channel_indices()]
        fs = 100
        frequencies, data = psd(rolled_data, Fs=fs)
        # Make it into a time series
        coords = {'channels': channels,
                  'epochs': np.arange(data.shape[1]),
                  'frequency': frequencies,
                  'samplerate': fs}
        dims = ['channels', 'epochs', 'frequency']
        ts = TimeSeriesLF(data, dims=dims, coords=coords)
        ts = ts[:,:,1:41] # Only need frequencies between 1:40Hz
        return ts


    ########### NORMALIZATION STATIC METHODS ###########
    @staticmethod
    def _normalize_min_to_max(array, minimum, maximum):
        # Normalize channels to between .0 and +1.0
        return (array - minimum) / (maximum - minimum)

    @staticmethod
    def _normalize_zero_to_high(data, high=100, axis=-1):
        """ Normalize data to values between 0 and high

        Parameters
        ----------
        data: np.array,
              data to normalize
        high: int, by default 100,
              value to set as the relative maximum
        axis: int, by default -1,
              axis over which to apply normalization

        Returns
        -------
        inputted data normalized between 0 and high
        """
        c_ = np.array(data)
        arr = c_.T * np.array([high]) / np.max(np.abs(c_), axis=axis)
        return arr.T

    @staticmethod
    def _normalize_by_integral(timeseries, dx=1., axis=1):
        """Apply an integral to normalize a given timeseries

        Parameters
        ----------
        timeseries: TimeSeriesLF,
                    time series data to normalize
        dx: float, default=1.,
            step over which to integrate on y
        axis: int, by default -1,
            axis over which to integrate

        Returns
        -------
        normalized: TimeSeriesLF,
                    time series data normalized
        """
        integral = VigilanceIndexPipeline._integrate(timeseries, dx=dx, axis=axis)
        # Norm so each ch sums to 1
        # TODO: this could be done more intelligently.
        if axis == 0:
            normalized = timeseries / integral[np.newaxis, :, :]
        elif axis == 1:
            normalized = timeseries / integral[:, np.newaxis, :]
        elif axis == 2:
            normalized = timeseries / integral[:, :, np.newaxis]
        return normalized

    ########### GENERAL UTILITY STATIC METHODS ###########

    @staticmethod
    def _integrate(y, dx=1., axis=1):
        """Calculates the discrete integral along the given axis using the composite trapezoidal rule

        Parameters
        ----------
        y: array-like
            input array for integral
        dx: float, default=1.,
            step over which to integrate on y
        axis: int, by default -1,
            axis over which to integrate

        Returns
        -------
        integral: array-like
                  shape = (y.shape[:-1])
        """
        integral = np.trapz(y=y, dx=dx, axis=axis)
        return integral

    @staticmethod
    def valid_band(freq, low, high):
        """Given an array of frequencies return a boolean array that is True bounded between high and low

        Parameters
        ----------
        freq: np.array like,
              array of frequency values
        low: int,
             lower bound of desired frequency range
        high: int,
              upper bound of desired frequency range

        Returns
        -------
        boolean_array of valid boundaries
        """
        return (freq >= low) & (freq <= high)

    @staticmethod
    def frequencies_into_bands(timeseries, how='sum'):
        """Convert frequencies into bands using either the frequencies mean or sum

        Parameters
        ----------
        timeseries: TimeSeriesLF
        how: str, by default 'sum',
             valid = 'sum', 'mean'

        Returns
        -------
        dat: TimeSeriesLF, data averaged into bands
        """
        frequency_bands = VigilanceIndexPipeline.VI_frequency_bands
        dat = []
        for k,v in enumerate(frequency_bands):
            _freqs = VigilanceIndexPipeline.valid_band(timeseries.frequency.data, *frequency_bands[v])
            if how == 'sum':
                dat.append(timeseries.sel(frequency=_freqs).sum('frequency'))
            elif how == 'mean':
                dat.append(timeseries.sel(frequency=_freqs).mean('frequency'))
        dat = TimeSeriesLF.concat(dat, dim='frequency')
        dat['frequency'] = list(frequency_bands.keys())
        return dat
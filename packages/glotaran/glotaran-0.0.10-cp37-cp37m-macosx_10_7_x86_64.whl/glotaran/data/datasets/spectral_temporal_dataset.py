from typing import Union, List

import numpy as np

from glotaran.model import Dataset


class SpectralTemporalDataset(Dataset):
    """
    Implementation of model.Dataset for spectral and temporal models.
    Provides a time and a spectral axis.
    """

    def __init__(self, time_unit: str = "s", spectral_unit: str = "nm"):
        self.time_unit = time_unit
        self.spectral_unit = spectral_unit
        super(SpectralTemporalDataset, self).__init__()

    _time_units = {
        "h":   3600,
        "m":     60,
        "s":      1,
        "ms":  1e-3,
        "us":  1e-6,
        "ns":  1e-9,
        "ps":  1e-12,
        "fs":  1e-15,
    }

    supported_time_units = [u for u in _time_units]
    """supported timeunits """

    _spectral_units = {
        "um":     1e3,
        "nm":       1,
        "cm^-1": 10e6,
    }

    supported_spectral_units = [u for u in _spectral_units]
    "supported spectral units"

    @property
    def time_unit(self) -> str:
        """the time unit [default 's'] """
        return self._time_unit

    @time_unit.setter
    def time_unit(self, value: str):
        if value not in self._time_units:
            raise ValueError("Unknown time unit {}. Supported units are "
                             "{}".format(value, self.supported_time_units))
        self._time_unit = value

    def get_time_axis(self, unit: str = None) -> Union[List, np.ndarray]:
        """
        Returns the time axis, does unit conversion if necessary

        Parameters
        ----------
        unit: str, default None
            the desired time unit

        Returns
        -------
        The (converted) time axis
        """
        if unit is None or unit == self.time_unit:
            return self.get_axis("time")
        conversion = self._time_units[self.time_unit] / self._time_units[unit]
        return conversion * self.get_axis("time")

    @property
    def time_axis(self, unit=None):
        return self.get_axis("time")

    @time_axis.setter
    def time_axis(self, value: Union[List, np.ndarray]):
        self.set_axis("time", value)

    @property
    def spectral_unit(self):
        """the spectral unit [default: 'nm'] """
        return self._spectral_unit

    @spectral_unit.setter
    def spectral_unit(self, value: str):
        if value not in self._spectral_units:
            raise ValueError("Unknown spectral unit {}. Supported units are "
                             "{}".format(value, self.supported_spectral_units))
        self._spectral_unit = value

    def get_spectral_axis(self, unit=None):
        """
        spectral axis

        Parameters
        ----------
        unit: str, default None

        Returns
        -------

        """
        if unit is None or unit == self.spectral_unit:
            return self.get_axis("spectral")

        if self.spectral_unit in ["nm", "um"]:
            if unit == "cm^-1":
                conversion = self._spectral_units["cm^-1"] * \
                    self._spectral_units[self.spectral_unit]
                return [conversion/v for v in self.get_axis("spectral")]
            conversion = self._spectral_units[self.spectral_unit] / \
                self._spectral_units[unit]
            return conversion * self.get_axis("spectral")
        conversion = self._spectral_units["cm^-1"] / \
            self._spectral_units[self.spectral_unit]
        return [conversion/v for v in self.get_axis("spectral")]

    @property
    def spectral_axis(self, unit: str = None):
        """the spectral axis """
        return self.get_axis("spectral")

    @spectral_axis.setter
    def spectral_axis(self, value: Union[List, np.ndarray]):
        self.set_axis("spectral", value)

    def get_estimated_axis(self):
        """the spectral axis """
        return self.spectral_axis

    def get_calculated_axis(self):
        """the time axis  """
        return self.time_axis

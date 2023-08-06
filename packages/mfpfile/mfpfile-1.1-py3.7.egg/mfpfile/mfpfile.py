from igor.binarywave import load
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)

class MFPFile:

    def __init__(self, fname):
        self.ibw = load(fname)
        self.wave_data = self.ibw['wave']['wData']
        self.label_list = None
        for label_list in self.ibw['wave']['labels']:
            if len(label_list) > 0:
                if self.label_list is None:
                    self.label_list = label_list
                else:
                    msg = "Expected only one list of labels not empty. Don't know how to "
                    msg += "handle this case."
                    raise NotImplementedError(msg)
        if self.label_list is None:
            self.label_list = []
        self.label_list = [lbl.decode('ISO-8859-1') for lbl in self.label_list if lbl]
        self.parameters = {}
        self._parse_note_to_parameter_dictionary()
        self.segment_indices = []
        self.n_segments = 0
        if not self.is_mfp_map():
            self._parse_segment_indices_to_list()

    def get_conversion_parameters(self):
        conversion_parameters = {"volts_to_meter": float(self.parameters['InvOLS']),
                                 "spring_constant": float(self.parameters['SpringConstant'])}
        return conversion_parameters
            
    def get_time_array(self, segment: int=None) -> np.ndarray:
        if self.is_mfp_map():
            raise RuntimeError("can't get time stamp array for maps")
        points_per_sec = int(self.parameters['NumPtsPerSec'])        
        if self.is_mfp_map():
            msg = "get_time_array only possible for force distance curves, "
            msg += "not for force maps!"
            raise NotImplementedError(msg)
        t = np.arange(self.wave_data.shape[0], dtype='float') / points_per_sec
        if segment is None:
            return t
        segment_indices = self._get_indices_of_segment(segment)
        return t[segment_indices[0]: segment_indices[1]]    
    
    def get_channel_by_name(self, channel_name: str, segment: int=None) -> np.ndarray:
        index = self._channel_name_to_index(channel_name)
        return self.get_channel_by_index(index, segment)

    def get_channel_by_index(self, channel_index: int, segment: int=None) ->np.ndarray:
        if self.wave_data.ndim == 1:
            data = self.wave_data
        else:
            data = self.wave_data.T[channel_index]
        if segment is None:
            return data
        segment_indices = self._get_indices_of_segment(segment)
        return data[segment_indices[0]: segment_indices[1]]    
    
    def _get_indices_of_segment(self, segment: int) -> List[int]:
        return [self.segment_indices[segment], self.segment_indices[segment + 1]]

    def _parse_note_to_parameter_dictionary(self):
        self.parameters = {}
        note_text = self.ibw['wave']['note'].decode('ISO-8859-1')
        for line in note_text.splitlines():
            if not line:
                continue
            key, value = line.split(':', 1)
            self.parameters[key] = value            

    def _parse_segment_indices_to_list(self):
        self.segment_indices = []
        indices_string = self.parameters['Indexes']
        for index in indices_string.split(','):
            if index:
                self.segment_indices.append(int(index))
        try:
            self.n_segments = int(self.parameters['NumOfSegments'])
        except KeyError:
            msg = "No Parameter labeled NumOfSegments found, will try "
            msg += "to infer number of segments from list of segment indices"
            logger.warn(msg)
            self.n_segments = len(self.segment_indices) - 1

    def __getitem__(self, channel_identifier) -> np.ndarray:
        if isinstance(channel_identifier, tuple):
            channel_identifier, segment = channel_identifier
        else:
            segment = None
        if isinstance(channel_identifier, int):
            return self.get_channel_by_index(channel_identifier, segment)
        if isinstance(channel_identifier, str):
            if channel_identifier == 'time':
                return self.get_time_array(segment)
            return self.get_channel_by_name(channel_identifier, segment)
        msg = "use get item with channel name (str) or channel index (int) only, "
        msg += "channel_identifier you provided has type " + str(type(channel_identifier))        
        raise TypeError(msg)

    def _channel_name_to_index(self, channel_name: str) -> int:        
        if channel_name in self.label_list:
            return self.label_list.index(channel_name)
        msg = "no channel with label " + channel_name + " found, candidates are:\n" \
              + ", ".join(self.label_list)
        raise ValueError(msg)

    def is_mfp_map(self) -> bool:
        return len(self.wave_data.shape) > 2

import numpy as np
import scipy.stats as st

class flags():
    def __init__(self):
        self.time_between_flag_dist = None
        self.duration_of_flag_dist = None

    def build_time_between_pdf(self, data):
        m = data.mean()
        s = data.std()
        self.time_between_flag_dist = st.norm(loc = m, scale = s)

    def build_duration_pdf(self, data):
        m = data.mean()
        s = data.std()
        self.duration_of_flag_dist = st.norm(loc = m, scale = s)

    def is_yellow_flag(self, time):
        rounded_to_sec = round(time,0)
        pdf_val = self.time_between_flag_dist.pdf(rounded_to_sec)
        return_value = False
        if pdf_val > 0.5:
            return_value = True
        return(return_value)
    
    def is_yellow_flag_done(self, time):
        rounded_to_sec = round(time,0)
        pdf_val = self.duration_of_flag_dist.pdf(rounded_to_sec)
        return_value = False
        if pdf_val > 0.5:
            return_value = True
        return(return_value)
    
    
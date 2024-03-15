import tabula
import pandas as pd

tabula.convert_into("data/pit_stop_time_cards.pdf", "data/pit_stop_time_cards.csv", output_format="csv", pages="all")
from CaculateEnergyLib.protein_class import Protein
from CaculateEnergyLib.dict_output import make_dictionary
from CaculateEnergyLib.dataframefunction import check_if_crd, final_comparison_df
import CaculateEnergyLib.ecalc as e
from CaculateEnergyLib.Funcs import *
import os
from timeit import default_timer as timer
import numpy as np
import json
import csv
import pandas as pd
pandasDF = frames("./", "model3.crd")
pandasDF.to_csv("out.csv")
protein_energy, vdw_energies, solvation_energies = e.energy(pandasDF)
print(protein_energy)
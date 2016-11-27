# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 18:14:04 2016

@author: noore
"""

from thermodynamics_for_cobra import reaction_thermodynamics
from cobra.io.sbml import create_cobra_model_from_sbml_file
import pandas as pd

fname = 'kochanowski_iJO1366_reactions_with_full_metabolome_coverage.csv'

karl_df = pd.DataFrame.from_csv('../data/' + fname,
                                index_col=0, header=0)
                                
from model_addons import add_to_model
model_fname = "../data/iJO1366.xml"
model = create_cobra_model_from_sbml_file(model_fname)
add_to_model(model)
rxns = map(model.reactions.get_by_id, karl_df.index)
Th = reaction_thermodynamics(rxns)
                      
karl_df[r"dG'0"] = map(lambda x: x.n, Th.dG0_prime)
karl_df[r"dG'0"] = karl_df[r"dG'0"].round(1)
karl_df[r"95% confidence"] = map(lambda x: x.s, Th.dG0_prime)
karl_df[r"95% confidence"] = karl_df[r"95% confidence"].round(1)

karl_df.to_csv('../res/' + fname)
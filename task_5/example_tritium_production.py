#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt

breeder_material = openmc.Material(1, "PbLi") #Pb84.2Li15.8 with 90% enrichment of Li6

enrichment_fraction = 0.9

breeder_material.add_element('Pb', 84.2,'ao')
breeder_material.add_nuclide('Li6', enrichment_fraction*15.8, 'ao')
breeder_material.add_nuclide('Li7', (1-enrichment_fraction)*15.8, 'ao')
breeder_material.set_density('atom/b-cm',3.2720171e-2)

mats = openmc.Materials([breeder_material])
mats.export_to_xml()
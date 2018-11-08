import openmc
import openmc.model
import os
import matplotlib.pyplot as plt

outer=10
rad=[3,4]
#MATERIALS#

min = 1
max = outer


R1 = rad[0]
R2 = rad[1]

mats = openmc.Materials()

tungsten = openmc.Material(name='Tungsten')
tungsten.set_density('g/cm3', 19.0)
tungsten.add_element('W', 1.0)
mats.append(tungsten)

water = openmc.Material(name='Water')
water.set_density('g/cm3', 1.0)
water.add_element('H', 2.0)
water.add_element('O', 1.0)
mats.append(water)

eurofer = openmc.Material(name='EUROFER97')
eurofer.set_density('g/cm3', 7.75)
eurofer.add_element('Fe', 89.067, percent_type='wo')
eurofer.add_element('C', 0.11, percent_type='wo')
eurofer.add_element('Mn', 0.4, percent_type='wo')
eurofer.add_element('Cr', 9.0, percent_type='wo')
eurofer.add_element('Ta', 0.12, percent_type='wo')
eurofer.add_element('W', 1.1, percent_type='wo')
eurofer.add_element('N', 0.003, percent_type='wo')
eurofer.add_element('V', 0.2, percent_type='wo')
mats.append(eurofer)

boron = openmc.Material(name='Boron')
boron.set_density('g/cm3', 2.37)
boron.add_element('B', 1.0)
mats.append(boron)

#GEOMETRY#

sphere1 = openmc.Sphere(R=min)
sphere2 = openmc.Sphere(R=R1)
sphere3 = openmc.Sphere(R=R2)
sphere4 = openmc.Sphere(R=max)
sphere5 = openmc.Sphere(R=15)
sphere6 = openmc.Sphere(R=17, boundary_type='vacuum')

vac1 = -sphere1
mat1 = +sphere1 & -sphere2
mat2 = +sphere2 & -sphere3
mat3 = +sphere3 & -sphere4
vac2 = +sphere4 & -sphere5
steel = +sphere5 & -sphere6
vac3 = +sphere6

vacuum1 = openmc.Cell(region=vac1)
first = openmc.Cell(region=mat1)
first.fill = tungsten
second = openmc.Cell(region=mat2)
second.fill = water
third = openmc.Cell(region=mat3)
third.fill = tungsten
vacuum2 = openmc.Cell(region=vac2)
vessel = openmc.Cell(region=steel)
vessel.fill = boron
vacuum3 = openmc.Cell(region=vac3)

root = openmc.Universe(cells=(vacuum1, first, second, third, vacuum2, vessel, vacuum3))

print(help(openmc.Universe.plot))

plt.show(root.plot(width=(max*2.1,max*2.1),
                   basis='xz'))
plt.show(root.plot(width=(max*2.1,max*2.1),basis='xy'))
plt.show(root.plot(width=(max*2.1,max*2.1),basis='yz'))

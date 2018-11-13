# Fusion Neutronics workshop with OpenMC
A selection of resources for learning openmc with particular focus on simulations relevant for fusion energy.

Introduction slides https://slides.com/shimwell/neutronics_workshop

### Acknowledgments
Fred Thomas for providing examples from the Serpent workshop
Enrique Miralles Dolz for providing the CSG tokamak model


### Installation

The use of OpenMC for neutronics analysis requires several software packages and data. To avoid installation of these dependancies and compatability issues with different operating systems the entrie workshop is distributed as a portable Docker container. Therefore the installation process consists of two steps.

1. Install Docker CE ([windows](https://store.docker.com/editions/community/docker-ce-desktop-windows/plans/docker-ce-desktop-windows-tier?tab=instructions]) ,[linx]([https://docs.docker.com/install/linux/docker-ce/ubuntu/]), [mac]([https://store.docker.com/editions/community/docker-ce-desktop-mac]))
2. Pull the Docker images from the store by typing  the following command in a terminal window
```docker pull shimwell/openmc_docker```

### Running OpenMC with docker

Now that you have the Docker image you can run it by typing the following command in a terminal window.
```docker run -it openmc```

This should load up an Ubuntu Docker container with OpenMC, Python3, Paraview, nuclear data and other libraries.

### Getting started on the tasks

#### Task 1 - plot some fusion relevant cross sections

Knowing the interaction probabilities of the isotopes and materials within your model can help understand the simulation results. There are several online tools for plotting cross sections such as [ShimPlotWell]([http://www.cross-section-plotter.com]). OpenMC is also able to plot cross sections for isotopes and materials.

from inside the docker container navigate to the task_1 directory and open the first example python script

```cd task_1```

```atom example_isotope_plot.py```

OpenMC is well documented so if the script does not make sense take a look at the relevant [documentation]([???]). This script will plot a selection of isotopes and certain reactions.

```python3 example_isotope_plot.py```

You should see an interactive plot of the n,2n cross section for an isotopes of lead and beryllium. To add different reactions to the plot we would need the ENDF reaction number which standard available [here]([https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf]).

- Try adding the other lead isotopes to the plot.

- Try adding tritium production in Li6 and Li7 to the same plot.

The plot should now show fusion relevant interactions. These are important reactions for breeder blankets as they offer high probability of neutron multiplication and tritium production.

- Try editting ```example_isotope_plot.py``` so that it plots tritium production or neutron multiplication for all the stable isotopes.

Elemental properties can also be found with OpenMc. Try plotting tritium production and neutron multiplication using the ```example_element_plot.py``` script

A nice feature of OpenMc is that is can plot cross sections for more complete materials made from combinations of isotopes. Open the next example python script and edit the script so that it can plot the tritium production and use this to identify the best elements for tritium production and neutron production. Why we might want to avoid some of these elements?

```atom example_material_plot.py```


This file shows us how to plot tritium production in Li4SiO4 which is a candiate ceramic breeder blanket material. Try editting ```example_material_plot.py``` a
so that other candiate breeder materials ae added to the plot. Produce the plot with the command

```python3 example_material_plot.py```



#### Task 2 - building and visulising the model geometry

OpenMC can provide both 2D and 3D visulisations of the CSG geometry.

There are two methods of producing 2D slice views of the geometry

The first example 2D slice plot can be produced by running

```cd task_3```

```python3 example_geometry_viewer.py```

Views of the simple model from different angles should appear. Another example script which produces similar results but works better for large models.

```python3 example_geometry_viewer_fortran_version.py```

Now try adding a first wall and shielded central column to the model using the OpenMC [simple examples]([https://openmc.readthedocs.io/en/stable/examples/pincell.html#Defining-Geometry]) and the [documentmentation]([https://openmc.readthedocs.io/en/stable/usersguide/geometry.html]) for CSG opperations.

- Change the inner radius of the blanket to 500cm

- Change the thickness of the blanket to 100cm

- Try adding a 10cm thick first wall to the hollow sphere.

- Try adding a center column with a 100cm radius and a 40 cm shield.

- Try creating a material from pure copper and assign it to the central column

- Try creating a homogenised material from 10% water and 90% steel and assign it to the first wall and the shield.

- Color the geometry plots by material see the [documentation]([https://openmc.readthedocs.io/en/stable/usersguide/plots.html]) for an example


#### Task 3 - visulise some neutron tracks

The ```example_neutron_flux.py``` file contains a single material, simple hollow sphere geometry, a 14MeV point source and a mesh tally showing neutron flux. Try running this file.

```Python3 example_neutron_flux.py```

You should see the isotropic point source appearing allong with the simple sphere geometry.

- Try changing the "flux" tally for an "absorption" tally and rerun the simulation with the same command.

- Try changing the Li6 enrichment of the material and compare the absorption of neutrons with the natural Li6 enrichment.

There is another example neutron flux file with the simple tokamak geometry. Take a look at ```example_neutron_flux_tokamak.py``` and run the file.

```Python3 example_neutron_flux_tokamak.py```

The model still has a point source but now it is located at x=150 y=0 z=0 and central column shielding is noticeable on the flux, absorption and tritium production mesh tallies.

#### Task 4 - Find the neutron spectra (and leakage)



#### Task 5 - Find the tritium production



#### Task 6 - Find the DPA

#### Task 7 - Find the best material for a neutron shield

#### Task 8 - Optimise a breeder blanket for tritium production

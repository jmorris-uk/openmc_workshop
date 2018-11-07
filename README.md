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

from inside the docker container navigate to the task 1 directory

```cd task_1```

Open the first example python script

```atom example_isotope_plot.py```

OpenMC is well documented so if the script does not make sense take a look at the relevant [documentation]([???]). This script will plot a selection of isotopes and certain reactions.

Try running the script with Python3

```python3 example_isotope_plot.py```

You should see an interactive plot of the n,2n cross section for an isotope of Lead. To add different reactions to the plot we would need the ENDF reaction number which standard available [here]([https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf]).

Try adding the other lead isotopes and Be9 to the plot.
Try adding tritium production in Li6 and Li7 to the plot.

The plot should now show fusion relevant interactions. These are important reactions for breeder blankets as they offer high probability of neutron multiplication and tritium production. Can you guess which other isotopes offer a high chance of tritium production or neutron multiplication and why we might want to avoid such isotopes?

A nice feature of OpenMc is that is can plot cross sections for combinations of isotopes. Open the next example python script

```atom example_material_plot.py```

This file shows us how to plot tritium production in Li4SiO4 which is a candiate ceramic breeder blanket material. Try adding others Li2SiO3, Li2ZrO3, Li2TiO3 to the plot.

Produce the plot with the command

```python3 example_material_plot.py```



#### Task 2 - visulise the model geometry

OpenMC can provide both 2D and 3D visulisations of the CSG geometry. First 2d models can be produced ....

#### Task 3 - visulise some neutron tracks

#### Task 4 - Find the neutron spectra (and leakage)

#### Task 5 - Find the tritium production

#### Task 6 - Find the DPA

#### Task 7 - Find the best material for a neutron shield

#### Task 8 - Optimise a breeder blanket for tritium production

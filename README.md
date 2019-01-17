# Fusion Neutronics workshop with OpenMC
A selection of resources for learning OpenMC with particular focus on simulations relevant for fusion energy.

There are a few slides introducing the workshop https://slides.com/shimwell/neutronics_workshop



### Installation

The use of OpenMC for neutronics analysis requires several software packages and nuclear data. These have been installed in a Docker container. Therefore the installation process consists of two steps.

1. Install Docker CE [windows](https://store.docker.com/editions/community/docker-ce-desktop-windows/plans/docker-ce-desktop-windows-tier?tab=instructions) ,[linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/), [mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)
2. Pull the Docker images from the store by typing  the following command in a terminal window

```docker pull shimwell/openmc```

### Running OpenMC with docker

Now that you have the Docker image you can enable graphics linking between your os and docker then run the image by typing the following command in a terminal window.

```xhost local:root```

```docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix  -v $PWD:/openmc_workshop/swap_space -e DISPLAY=unix$DISPLAY -e OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml --privileged shimwell/openmc```

This should load up an Ubuntu 18.04 Docker container with OpenMC, Python3, Paraview, nuclear data and other libraries.

You can quickly test the graphics options worked by typing ```paraview``` in the docker container enviroment.

Also check if the workshop repository has been updated by typing the following command from within the Docker container.

```git pull```

If you have trouble with the git pull command this could be due to your OS not sharing the internet connection with the docker container. Sharing the internet connection can be encouraged with this modified run command.


```docker run --net=host -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/openmc_workshop/swap_space -e DISPLAY=unix$DISPLAY -e OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml --privileged shimwell/openmc```

The local directory that you run docker from will be mapped to the /openmc_workshop/swap_space folder within the docker container. This can be useful for transfering files from your docker to your local machine. 

### Getting started on the tasks

- [Task 1 - Cross section plotting](#task1)
- [Task 2 - Building and visualizing the model geometry](#task2)
- [Task 3 - Visualizing neutron tracks](#task3)
- [Task 4 - Finding the neutron flux](#task4)
- [Task 5 - Finding the neutron spectra](#task5)
- [Task 6 - Finding the tritium production](#task6)
- [Task 7 - Finding the neutron damage](#task7)
- [Task 8 - Optimize a breeder blanket for tritium production](#task8)


#### <a name="task1"></a>Task 1 - Cross section plotting

Please allow 20 minutes for this task.

Expected outputs from this task are on [slide 5 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/5)

Knowing the interaction probabilities of the isotopes and materials within your model can help understand the simulation results. There are several online tools for plotting nuclear cross sections such as [ShimPlotWell](http://www.cross-section-plotter.com). However OpenMC is also able to plot cross sections for isotopes and materials.

From inside the docker container navigate to the task_1 directory and open the first example python script

```cd tasks/task_1```

```atom example_isotope_plot.py```

OpenMC is well documented so if the script does not make sense take a look at the relevant [documentation](https://openmc.readthedocs.io/en/v0.10.0/examples/nuclear-data.html). This script will plot a selection of isotopes and certain reactions.

```python3 1_example_isotope_plot.py```

You should see an interactive plot of the n,2n cross section for isotopes of lead and beryllium. To add different reactions to the plot we would need the ENDF reaction number (MT number) which is available [here](https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf).

- Try adding the other lead isotopes to the plot.

- Try adding tritium production in Li6 and Li7 to the same plot.

The plot should now show fusion relevant interactions. These are important reactions for breeder blankets as they offer high probability of neutron multiplication and tritium production.

- Try editing ```1_example_isotope_plot.py``` so that it plots tritium production or neutron multiplication for all the stable isotopes.

Elemental properties can also be found with OpenMC. Try opening the script and then plotting tritium production and neutron multiplication using the ```2_example_element_plot.py``` script

```atom 2_example_element_plot.py```

```python3 2_example_element_plot.py```

A nice feature of OpenMC is that it can plot cross sections for more complete materials made from combinations of isotopes. Open the next example python script and edit the script so that it can plot the tritium production and use this to identify the best elements for tritium production and neutron production. Why we might want to avoid some of these elements?

```atom 3_example_material_plot.py```

This file shows us how to plot tritium production in Li4SiO4 which is a candidate ceramic breeder blanket material.

 - Try editing ```3_example_material_plot.py``` so that other candidate breeder materials are added to the plot.

 - Produce the plot with the command
```python3 3_example_material_plot.py```







#### <a name="task2"></a>Task 2 - Building and visualizing the model geometry.

Please allow 20 minutes for this task.

Expected outputs from this task are on [slide 6 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/6)

OpenMC can provide both 2D and 3D visualizations of the Constructive Solid Geometry ([CSG](https://en.wikipedia.org/wiki/Constructive_solid_geometry)).
There are two methods of producing 2D slice views of the geometry

The first example 2D slice plot can be opened and produced by running ...

```cd tasks/task_2```

```atom 1_example_geometry_viewer_2d.py```

```python3 1_example_geometry_viewer_2d.py```

Views of the simple model from different planes (xy, xz, zy) should appear. The second method of producing 2D slice plots works better for large models.

```atom 2_example_geometry_viewer_2d_fortran_version.py```

```python3 2_example_geometry_viewer_2d_fortran_version.py```

Now try adding a first wall and shielded central column to the model using the OpenMC [simple examples](https://openmc.readthedocs.io/en/stable/examples/pincell.html#Defining-Geometry) and the [documentation](https://openmc.readthedocs.io/en/stable/usersguide/geometry.html) for CSG operations.

- Change the inner radius of the blanket to 500cm

- Change the thickness of the blanket to 100cm

- Try adding a 10cm thick first wall to the hollow sphere.

- Try adding a centre column with a 100cm radius and a 40 cm shield.

- Try creating a material from pure copper and assign it to the central column

- Try creating a homogenized material from 10% water and 90% steel and assign it to the first wall and the shield.

- Colour the geometry plots by material see the [documentation](https://openmc.readthedocs.io/en/stable/usersguide/plots.html) for an example

By the time you have added you extra geometry components your solution should look similar to the geometry contained in the next example script.

```atom 3_example_geometry_viewer_2d_tokamak.py```

```python3 3_example_geometry_viewer_2d_tokamak.py```

The next example script shows a simple geometry that can be viewed in 3D using paraview. This converts the geometry into a block

```atom 4_example_geometry_viewer_3d.py ```

```python3 4_example_geometry_viewer_3d.py ```

Paraview should load up when this script completes. To make the geometry visible click the "Apply" button and also the small eye ball icon on the left hand side. Then select "id" and "surface" in the dropdown menus to view the geometry. Then use the threshold and slice operations to view the geometry.

- Try using the paraview threshold operation to remove the vacuum cell. Set the threshold to 0 then click the "Apply" button.

- Try combining the last two scripts so that you can visualize the tokamak model in 3D.

```atom 5_example_geometry_viewer_3d_tokamak.py ```

```python3 5_example_geometry_viewer_3d_tokamak.py ```






#### <a name="task3"></a>Task 3 - Visualizing neutron tracks

Please allow 20 minutes for this task.

Expected outputs from this task are on [slide 7 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/7)

When OpenMC runs a statepoint (output) file is produced which contains information on the neutron source, tally results and additional information. This task focuses on information on the neutron source tasks 4, 5 and 6 focus on extracting other information from the statepoint file.

The ```plot_neutron_birth_energy.py``` file shows you how to access the statepoint file created by a simulation. In this example the birth energy of all the simulated neutrons is extracted. A plot of the energy distribution and
run the ```plot_neutron_birth_energy.py``` script to produce the plot.

```python3 plot_neutron_birth_energy.py```

As you can see there is a mono-energetic energy source of 14MeV neutrons. There are two other source energy distributions available in the ```plot_neutron_birth_energy.py``` script.

- Try plotting the Watt and Muir neutron spectra and compare them to the mono energetic source.

- Try changing the Muir plasma temperature from 20KeV to 40KeV and plot the two distributions on the same figure.


In the next example the initial neutron trajectory and birth location is plotted. Again this information is accessed from the statepoint file.

Run ```python3 plot_neutron_birth_location.py``` to produce the plot

The ```example_neutron_tracks.py``` file contains a hollow sphere made of two materials and a 14MeV point source in the centre of the geometry. The objective of this task is to create some 3D particle tracks and visualize them with the geometry.

Open up ```atom example_neutron_tracks.py``` and take a look at the ```model.run(tracks=True)``` method. This argument results in the creation of a h5 file for each neutron simulated.

Run the script with the command
```python3 example_neutron_tracks.py```

Use paraview to load the geometry file and then open the track files (.vtp files). Parview can also be used to slice (slice this model on the z plane) and threshold the geometry. Looking at the tracks can you tell which material is water and which is zirconium?








#### <a name="task4"></a>Task 4 - Finding the neutron flux

Please allow 15 minutes for this task.

Expected outputs from this task are on [slide 8 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/8)

In this task mesh tallies will be produced and visualized.

The ```example_neutron_flux.py``` file contains a single material, simple hollow sphere geometry, a 14MeV point source and a mesh tally showing neutron flux. Try running this file.

```Python3 example_neutron_flux.py```

You should see the isotropic point source appearing along with the simple sphere geometry. The colour map shows the neutron flux reducing as one moves away from the point source.

- Try changing the "flux" tally for an "absorption" tally and rerun the simulation with the same command.

- Try changing the Li6 enrichment of the material and compare the absorption of neutrons with the natural Li6 enrichment.

There is another example neutron flux file with the simple tokamak geometry. Take a look at ```example_neutron_flux_tokamak.py``` and run the file with the command.

```atom example_neutron_flux_tokamak.py```

```Python3 example_neutron_flux_tokamak.py```

The model still has a point source but now it is located at x=150 y=0 z=0 and central column shielding is noticeable on the flux, absorption and tritium production mesh tallies.

- Try changing the mesh tally from (n,t) to flux and absorption.









#### <a name="task5"></a>Task 5 - Finding the neutron spectra

Please allow 15 minutes for this task.

Expected outputs from this task are on [slide 10 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/10)

In this task the neutron spectra at two different locations will be found and visualized.

Open ```example_neutron_spectra_tokamak.py``` to see how the neutron spectra is obtained for the breeder blanket cell. Then run ```example_neutron_spectra_tokamak.py``` to plot the neutron spectra within the breeder blanket.

```atom example_neutron_spectra_tokamak.py```

```Python3 example_neutron_spectra_tokamak.py```

- Try plotting the neutron spectra within the first wall cell on the same axis and compare it to the breeder blanket cell.







#### <a name="task6"></a>Task 6 - Finding the tritium production

Please allow 15 minutes for this task.

Expected outputs from this task are on [slide 11 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/11)

In this task you will find the tritium breeding ratio (TBR) for a single tokamak model using ```example_tritium_production.py``` and then the TBR values for a range of tokamak models with different Li6 enrichment values with the ```example_tritium_production_study.py``` script.

Open and run the ```example_tritium_production.py``` script with the following commands.

```atom example_tritium_production.py```

```Python3 example_tritium_production.py```

The example script prints the TBR and the associated error. As you can see the error is high.

- Try increasing the number of ```batches``` and the ```sett.particles``` and rerun the simulation. You should observe an improved estimate of TBR.

Your should find that the TBR value obtained from the improved simulation is below 1.0 so this design will not be self sufficient in fuel.

One option for increasing the TBR is to increase the Li6 content within the blanket. Open and run the next script and see how TBR changes as the Li6 enrichment is increased.

```atom example_tritium_production_study.py```

```Python3 example_tritium_production_study.py```

- Try changing '(n,t)' to 205 and you should get the same result as this is the equivalent  [ENDF MT reaction number](https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf)







#### <a name="task7"></a>Task 7 - Finding the neutron damage

Please allow 15 minutes for this task.

Expected outputs from this task are on [slide 12 of the presentation](https://slides.com/shimwell/neutronics_workshop/#/12)

Displacements per atom or DPA is one measure of damage within materials exposed to neutron irradiation. The MT reaction number is 444 so the example tritium production script from task 6 can be modified to find DPA / 444 instead of (n,t) / 205.

In the case of DPA a tally multiplier is needed to account for the material and recombination effects. For example different atoms require different amounts of energy to [displace](https://fispact.ukaea.uk/wiki/Output_interpretation#DPA_and_KERMA).
 Without going into detail assume this is already incorporated into the tally result. The only multiplier needed is to multiply the result by the source intensity (in neutrons per second) and the irradiation duration (in seconds).

- Using this information find the DPA on the first wall for a 2GW (fusion power) reactor over a 5 year period. Does this exceed the Eurofer DPA limit of 70 DPA?



#### <a name="task8"></a>Task 8 - Optimize a breeder blanket for tritium production

Please allow 25 minutes for this task.

This task is more open ended and the aim is to find the minimum thickness of breeder material needed to obtain a TBR of 1.2.

There are several candidate breeder materials including a lithium ceramic (Li4SiO4), Flibe, Lithium lead (eutectic) and pure lithium.

Each material can have it's lithium 6 content enriched and this has an impact on the TBR.

Examine the ```simulate_tokamak_model.py``` file and try to understand how the model is created and particularly how the simulation parameters are saved in a .json file.

You will need to adjust some of the settings within the simulations (nps and batches) to make sure that the error on the final TBR values are acceptable.

Currently the input parameters for lithium 6 enrichment and blanket thickness are randomly sampled so you might want to change this as well.

First you will also need to change the surface definitions so that the geometry changes as thickness is varied when a new thickness is passed to the geometry making function.

There are two scripts to help you analysis the simulation results.

- ```plot_simulation_results_2d.py``` will allow you to see the impact of changing either the lithium 6 enrichment or the blanket thickness.

- ```plot_simulation_results_3d.py``` will allow you to see the combined impact of changing  the lithium 6 enrichment and the blanket thickness.

Ultimately you should come up with the minimal thickness needed for each candidate blanket material and the lithium 6 enrichment required at that thickness. Feel free to share simulation data with other groups and interpolate between the data points.

One option for interpolating the data is a [Gaussian process tool](https://github.com/C-bowman/inference_tools/blob/master/inference/gp_tools.py)


### Acknowledgments
Fred Thomas for providing examples from previous years Serpent workshop,
Enrique Miralles Dolz for providing the CSG tokamak model, Andrew Davis for his work on the fusion neutron source, Chris Bowman for his Gaussian process software and the OpenMC team for their software.

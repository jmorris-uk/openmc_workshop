# Fusion Neutronics workshop with OpenMC
A selection of resources for learning openmc with particular focus on simulations relevant for fusion energy.

There are a few slides introducing the workshop https://slides.com/shimwell/neutronics_workshop



### Installation

The use of OpenMC for neutronics analysis requires several software packages and nuclear data. These have been installed in a Docker container. Therefore the installation process of consists of two steps.

1. Install Docker CE ([windows](https://store.docker.com/editions/community/docker-ce-desktop-windows/plans/docker-ce-desktop-windows-tier?tab=instructions]) ,[linx]([https://docs.docker.com/install/linux/docker-ce/ubuntu/]), [mac]([https://store.docker.com/editions/community/docker-ce-desktop-mac]))
2. Pull the Docker images from the store by typing  the following command in a terminal window

```docker pull shimwell/openmc_docker```

### Running OpenMC with docker

Now that you have the Docker image you can run it by typing the following command in a terminal window.

```docker run -it openmc```

This should load up an Ubuntu Docker container with OpenMC, Python3, Paraview, nuclear data and other libraries.



### Getting started on the tasks

- [Task 1 - Cross section plotting](#task1)
- [Task 2 - Building and visualizing the model geometry](#task2)
- [Task 3 - Visualizing neutron tracks](#task3)
- [Task 4 - Finding the neutron spectra](#task4)
- [Task 5 - Finding the neutron spectra](#task5)
- [Task 6 - Finding the tritium production](#task6)
- [Task 7 - Finding the neutron damage](#task7)
- [Task 8 - Finding the best material for shielding neutrons](#task8)
- [Task 9 - Optimize a breeder blanket for tritium production](#task9)

#### <a name="task1"></a>Task 1 - Cross section plotting

Knowing the interaction probabilities of the isotopes and materials within your model can help understand the simulation results. There are several online tools for plotting nuclear cross sections such as [ShimPlotWell]([http://www.cross-section-plotter.com]). However OpenMC is also able to plot cross sections for isotopes and materials.

From inside the docker container navigate to the task_1 directory and open the first example python script

```cd tasks/task_1```

```atom example_isotope_plot.py```

OpenMC is well documented so if the script does not make sense take a look at the relevant [documentation]([https://openmc.readthedocs.io/en/v0.10.0/examples/nuclear-data.html]). This script will plot a selection of isotopes and certain reactions.

```python3 1_example_isotope_plot.py```

You should see an interactive plot of the n,2n cross section for an isotopes of lead and beryllium. To add different reactions to the plot we would need the ENDF reaction number which standard available [here]([https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf]).

- Try adding the other lead isotopes to the plot.

- Try adding tritium production in Li6 and Li7 to the same plot.

The plot should now show fusion relevant interactions. These are important reactions for breeder blankets as they offer high probability of neutron multiplication and tritium production.

- Try editing ```1_example_isotope_plot.py``` so that it plots tritium production or neutron multiplication for all the stable isotopes.

Elemental properties can also be found with OpenMc. Try opening the script and then plotting tritium production and neutron multiplication using the ```2_example_element_plot.py``` script

```atom 2_example_element_plot.py```

```python3 2_example_element_plot.py```

A nice feature of OpenMc is that is can plot cross sections for more complete materials made from combinations of isotopes. Open the next example python script and edit the script so that it can plot the tritium production and use this to identify the best elements for tritium production and neutron production. Why we might want to avoid some of these elements?

```atom 3_example_material_plot.py```

This file shows us how to plot tritium production in Li4SiO4 which is a candidate ceramic breeder blanket material.

 - Try editing ```3_example_material_plot.py``` so that other candidate breeder materials are added to the plot.

 - Produce the plot with the command
```python3 3_example_material_plot.py```







#### <a name="task2"></a>Task 2 - Building and visualizing the model geometry

OpenMC can provide both 2D and 3D visualizations of the Constructive Solid Geometry ([CSG](https://en.wikipedia.org/wiki/Constructive_solid_geometry)).
There are two methods of producing 2D slice views of the geometry

The first example 2D slice plot can be opened and produced by running ...

```cd tasks/task_2```

```atom 1_example_geometry_viewer_2d.py```

```python3 1_example_geometry_viewer_2d.py```

Views of the simple model from different planes (xy, xz, zy) should appear. The second method of producing 2D slice plots works better for large models.

```atom 2_example_geometry_viewer_2d_fortran_version.py```

```python3 2_example_geometry_viewer_2d_fortran_version.py```

Now try adding a first wall and shielded central column to the model using the OpenMC [simple examples]([https://openmc.readthedocs.io/en/stable/examples/pincell.html#Defining-Geometry]) and the [documentation]([https://openmc.readthedocs.io/en/stable/usersguide/geometry.html]) for CSG operations.

- Change the inner radius of the blanket to 500cm

- Change the thickness of the blanket to 100cm

- Try adding a 10cm thick first wall to the hollow sphere.

- Try adding a center column with a 100cm radius and a 40 cm shield.

- Try creating a material from pure copper and assign it to the central column

- Try creating a homogenized material from 10% water and 90% steel and assign it to the first wall and the shield.

- Color the geometry plots by material see the [documentation]([https://openmc.readthedocs.io/en/stable/usersguide/plots.html]) for an example

By the time you have added you extra geometry components your solution should look similar to the geometry contained in the next example script.

```atom 3_example_geometry_viewer_2d_tokamak.py```

```python3 3_example_geometry_viewer_2d_tokamak.py```

The next example script shows a simple geometry that can be viewed in 3D using paraview. This converts the geometry into a block

```atom 4_example_geometry_viewer_3d.py ```

```python3 4_example_geometry_viewer_3d.py ```

select "id" and "surface" in the dropdown menus and click apply to view the geometry. Then use the threshold and slice operations to view the geometry.

- Try combining the last two scripts so that you can visualize the tokamak model in 3D.

```atom 5_example_geometry_viewer_3d_tokamak.py ```

```python3 5_example_geometry_viewer_3d_tokamak.py ```

#### <a name="task3"></a>Task 3 - Visualizing neutron tracks

When OpenMC runs a statepoint file is produce which contains information on the neutron source, tally results and additional information. This task focuses on information on the neutron source tasks 4, 5 and 6.

The ```plot_neutron_birth_energy.py``` file shows you how to access the statepoint file created by a simulation. In this example the birth energy of all the simulated neutrons is extracted. A plot of the energy distribution and

Run ```python3 plot_neutron_birth_energy.py``` to produce the plot.

In the next example the initial neutron trajectory and birth location is plotted. Again this information is accessed from the statepoint file.

Run ```python3 plot_neutron_birth_location.py``` to produce the plot

The ```example_neutron_tracks.py``` file contains a hollow sphere made of two materials and a 14MeV point source in the center of the geometry. The objective of this task is to create some 3D particle tracks and visualize them with the geometry.

Open up ```atom example_neutron_tracks.py``` and take a look at the ```model.run(tracks=True)``` method. This argument results in the creation of a h5 file for each neutron simulated.

Run the script with the command
```python3 example_neutron_tracks.py```

Use paraview to load the geometry file and then import the track files (.vtp files). Parview can also be used to slice (slice this model on the z plane) and threshold the geometry. Looking at the tracks can you tell which material is water and which is zirconium.

#### <a name="task4"></a>Task 4 - Finding the neutron flux

In this task mesh tallies will be produced and visualized.

The ```example_neutron_flux.py``` file contains a single material, simple hollow sphere geometry, a 14MeV point source and a mesh tally showing neutron flux. Try running this file.

```Python3 example_neutron_flux.py```

You should see the isotropic point source appearing along with the simple sphere geometry. The color map shows the neutron flux reducing as one moves away from the point source.

- Try changing the "flux" tally for an "absorption" tally and rerun the simulation with the same command.

- Try changing the Li6 enrichment of the material and compare the absorption of neutrons with the natural Li6 enrichment.

There is another example neutron flux file with the simple tokamak geometry. Take a look at ```example_neutron_flux_tokamak.py``` and run the file with the command.

```atom example_neutron_flux_tokamak.py```

```Python3 example_neutron_flux_tokamak.py```

The model still has a point source but now it is located at x=150 y=0 z=0 and central column shielding is noticeable on the flux, absorption and tritium production mesh tallies.

- Try changing the mesh tally from (n,t) to flux and absorption.

#### <a name="task5"></a>Task 5 - Finding the neutron spectra

In this task the neutron spectra at two different locations will be found and visualized.

Open ```example_neutron_spectra_tokamak.py``` to see how the neutron spectra is obtained for the breeder blanket cell. Then run ```example_neutron_spectra_tokamak.py``` to plot the neutron spectra within the breeder blanket.

```atom example_neutron_spectra_tokamak.py```

```Python3 example_neutron_spectra_tokamak.py```

- Try plotting the neutron spectra within the first wall cell on the same axis and compare it to the breeder blanket cell.



#### <a name="task6"></a>Task 6 - Finding the tritium production

In this task you will find the tritium breeding ratio (TBR) for a single tokamak model using ```example_tritium_production.py``` and then the TBR values for a range of tokamak models with different Li6 enrichment values with the ```example_tritium_production_study.py``` script.

Open and run the ```example_tritium_production.py``` script with the following commands.

```atom example_tritium_production.py```

```Python3 example_tritium_production.py```

The TBR value obtained from the simulation is printed in the terminal. Notice that the TBR is below 1.0 so this design will not be self sufficient in fuel.

One option for increasing the TBR is to increase the Li6 content within the blanket. Open and run the next script and see how TBR changes as the Li6 enrichment is increased.

```atom example_tritium_production_study.py```

```Python3 example_tritium_production_study.py```

- Try changing '(n,t)' to 205 and you should get the same result as this is the equivelent  [ENDF MT reaction number]([https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf])

#### <a name="task7"></a>Task 7 - Finding the neutron damage

Displacements per atom or DPA is one measure of damage within materials exposed to neutron irradiation. The MT reaction number is 444 so the example tritium production script from task 6 can be modified to find DPA / 444 instead of (n,t) / 205.

An arbitrary tally multiplier is needed

[DPA values]([https://fispact.ukaea.uk/wiki/Output_interpretation#DPA_and_KERMA])

#### <a name="task8"></a>Task 8 - Finding the best material for shielding neutrons

#### <a name="task9"></a>Task 9 - Optimize a breeder blanket for tritium production


### Acknowledgments
Fred Thomas for providing examples from the Serpent workshop
Enrique Miralles Dolz for providing the CSG tokamak model

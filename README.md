# Fusion Neutronics workshop with OpenMC
A selection of resources for learning openmc with particular focus on simulations relevant for fusion energy.

Introduction slides https://slides.com/shimwell/neutronics_workshop

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

#### Task 2 - visulise the model geometry

OpenMC can provide both 2D and 3D visulisations of the CSG geometry. First 2d models can be produced ....

#### Task 3 - visulise some neutron tracks

#### Task 4 - Find the neutron spectra (and leakage)

#### Task 5 - Find the tritium production

#### Task 6 - Find the DPA

#### Task 7 - Find the best material for a neutron shield

#### Task 8 - Optimise a breeder blanket for tritium production

FROM ubuntu:18.04

MAINTAINER Jonathan Shimwell

# This docker image contains all the dependencies required to run OpenMC.
# More details on OpenMC are available on the web page https://openmc.readthedocs.io

# build with
#     sudo docker build -t shimwell/openmc:latest .
# run with
#     docker run --net=host -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/openmc_workshop/swap_space -e DISPLAY=unix$DISPLAY -e OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml --privileged shimwell/openmc
# if you have no GUI in docker try running this xhost command prior to running the image
#     xhost local:root
# push to docker store with
#     docker login
#     docker push shimwell/openmc:latest
#



# Install additional packages

RUN apt-get --yes update && apt-get --yes upgrade

RUN apt-get --yes install gfortran g++ cmake libhdf5-dev git

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y python3-tk


# Python Prerequisites Required
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install six
RUN pip3 install h5py
RUN pip3 install Matplotlib
RUN pip3 install uncertainties
RUN pip3 install lxml
RUN pip3 install scipy

# Python Prerequisites Optional
RUN pip3 install cython
RUN pip3 install vtk
RUN apt-get install --yes libsilo-dev
RUN pip3 install pytest
RUN pip3 install codecov
RUN pip3 install pytest-cov
RUN pip3 install pylint

# Python libraries used in the workshop
RUN pip3 install plotly
RUN pip3 install tqdm


# installs OpenMc from source (modified version which includes more MT numbers in the cross sections)
# RUN git clone https://github.com/mit-crpg/openmc && \
RUN git clone https://github.com/Shimwell/openmc.git && \
    cd openmc && \
    git checkout added_MT_gas_reactions_back && \
    mkdir bld && cd bld && \
    cmake .. -DCMAKE_INSTALL_PREFIX=.. && \
    make && \
    make install

RUN PATH="$PATH:/openmc/bld/bin/"
RUN cp /openmc/bld/bin/openmc /usr/local/bin

RUN cd openmc && python3 setup.py install

RUN cd openmc && python3 /openmc/scripts/openmc-get-nndc-data -b

# installs the Atom text editor
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:webupd8team/atom
RUN apt update
RUN apt install -y atom

RUN apt-get install -y firefox


RUN OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml

RUN export OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml

RUN apt-get --yes update
RUN apt-get --yes install hdf5-tools
RUN apt-get --yes install imagemagick
RUN apt-get --yes install paraview


RUN echo 'alias python="python3"' >> ~/.bashrc

RUN git clone https://github.com/Shimwell/openmc_workshop.git

WORKDIR /openmc_workshop

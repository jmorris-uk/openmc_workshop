FROM ubuntu:16.04

MAINTAINER Jonathan Shimwell  

# This docker image contains all the dependencies required to run OpenMC.
# More details on OpenMC are avaiallbe on the webpage
# https://openmc.readthedocs.io

# build with
#     sudo docker build -t shimwell/openmc:latest .
# run with
#     docker run -it -e DISPLAY=$DISPLAY  shimwell/openmc 
#     docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY shimwell/openmc
#     docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v ~/Desktop/openmc_workshop:/local shimwell/openmc
# if you have no GUI in docker try running 
#     xhost local:root
# push to docker store with 
#     docker login
#     docker push shimwell/openmc:latest
#



# Install additional packages

RUN apt-get --yes update && apt-get --yes upgrade

RUN apt-get --yes install gfortran g++ cmake libhdf5-dev git

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev python3-tk 
#  && cd /usr/local/bin \
#  && ln -s /usr/bin/python3 python \
#  && pip3 install --upgrade pip

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


# installs OpenMc from source
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

#RUN cd openmc && python3 /openmc/scripts/openmc-get-nndc-data --libver latest
#RUN cd openmc && python3 /openmc/scripts/openmc-get-nndc-data --libver earliest

#COPY ENDF-B-VII.1-neutron-293.6K.tar.gz .
#COPY ENDF-B-VII.1-tsl.tar.gz .

# # installs text editor Atom
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:webupd8team/atom
RUN apt update
RUN apt install -y atom

RUN apt-get install -y firefox


RUN OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml

RUN export OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml


RUN apt-get install hdf5-tools

COPY tasks /
#REPLACE WITH GIT PULL

#RUN "export OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml" >> /root/.bashrc

WORKDIR /


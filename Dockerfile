FROM ubuntu:16.04

MAINTAINER Jonathan Shimwell  

# This docker image contains all the dependencies required to run OpenMC.
# More details on OpenMC are avaiallbe on the webpage
# https://openmc.readthedocs.io

# build with
#     sudo docker build -t shimwell/openmc:latest .
# run with
#     docker run -it shimwell/openmc 
# push to docker store with 
#     docker login
#     docker push shimwell/openmc:latest



# Install additional packages

RUN apt-get --yes update && apt-get --yes upgrade

RUN apt-get --yes install gfortran g++ cmake libhdf5-dev git

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3-tk \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


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

RUN pip3 install plotly

RUN git clone https://github.com/mit-crpg/openmc && \
    cd openmc && \
    mkdir bld && cd bld && \
    cmake .. -DCMAKE_INSTALL_PREFIX=.. && \
    make -j8 && \
    make install

RUN cd openmc && python3 setup.py install

RUN PATH="$PATH:$openmc/bld/bin/"

RUN python3 /openmc/scripts/openmc-get-nndc-data -b

RUN OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml

COPY task_1 task_1
#REPLACE WITH GIT PULL


WORKDIR /


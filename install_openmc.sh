
#this script will install OpenMC to the /opt/openmc directory on ubuntu 18.04

sudo apt-get --yes update
sudo apt-get --yes upgrade

sudo apt-get --yes install gfortran g++ cmake libhdf5-dev git

cd /opt
git clone https://github.com/mit-crpg/openmc
cd openmc
mkdir bld
cd bld
cmake .. -DCMAKE_INSTALL_PREFIX=..
make -j8
make install

sudo apt-get --yes install python3-pip python3-tk

sudo pip3 install --upgrade pip

# Python Prerequisites Required
pip3 install numpy --user
pip3 install pandas --user
pip3 install six --user
pip3 install h5py --user
pip3 install Matplotlib --user
pip3 install uncertainties --user
pip3 install lxml --user
pip3 install scipy --user

# Python Prerequisites Optional
pip3 install Cython==0.28.5 --user
pip3 install vtk
sudo apt-get install --yes libsilo-dev
pip3 install pytest

pip3 install codecov --user
pip3 install pytest-cov --user
pip3 install pylint --user

cd /opt/openmc
sudo python3 setup.py install ## pip install might work betters
sudo cp /opt/openmc/bin/openmc /usr/bin

sudo python3 /opt/openmc/scripts/openmc-get-nndc-data -b

export OPENMC_CROSS_SECTIONS=/opt/openmc/nndc_hdf5/cross_sections.xml

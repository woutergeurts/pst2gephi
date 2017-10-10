sudo apt-get -y update 
sudo apt-get install autoconf automake autopoint libtool pkg-config
sudo apt-get install build-essential debhelper fakeroot autotools-dev zlib1g-dev python-all-dev 
sudo apt-get install dh-autoreconf zlib1g-dev python3-dev
sudo apt-get install libpff-dbg

# cd libpyff

# ./synclibs.sh
# ./autogen.sh
# ./configure --enable-python

# system_string_vsnprintf does not exist (replace with ordinary vsnprintf)

echo export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/lib >> $HOME/.bashrc

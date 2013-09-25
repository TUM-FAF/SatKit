#SatKit project
_version_ alfa.0.0

Purpose of this work is to construct ground tracks for artificial satellites. 
This script takes data from TLE files which can be found on the internet, and
according to the parameters of the satellite it computes current position, in
several coordinate frames, and it also can compute velocity, need to add few 
lines of code.

### Installing on Ubuntu

    git clone git@github.com:TUM-FAF/SatKit.git
    sudo apt-get build-dep python-imaging
    sudo apt-get install libjpeg62 libjpeg62-dev python-imaging-tk


### Running
requirements:
+ python2.7
+ Python Imaging Library

```
$ python moin.py
```

there are already tle data, for some recent launched satellites, they can be 
tracked adding their index from tle file, or changing the url from track.py.

_there may be some difference between output of the script and real data_

###To do:
* compute difference of time for real time animation **done**
* 'translate' algorithm for computing position vector **done**
* improve algorithm, quaternions or Gibbs 
* choose an good gui constructor = _Tkinter,_ нет "програмированию" мышкой
* clean code 
* read from the webserver TLE **done**
* compute position from TLE **done**
* integrate with time
* synchronize satellite with real time 
* find a better way of representing tracks(earth is spheric, 
    map is rectangular)


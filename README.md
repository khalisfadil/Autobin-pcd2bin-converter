# Nuscene structure Dataset Preparing
In this repository, the lidar data from Autobin is decoded into a new dataset structure which almost similar to the Nuscene structure by using a Python3.

## Installation
This repository is using python virtual environment(optional)
```bash
python3 -m venv venv
source venv/bin/acticate
``` 
### Dependencies
```bash
pip install numpy
pip install shutil
pip install pickle-mixin
pip install open3d
pip install --user git+https://github.com/DanielPollithy/pypcd.git
```
go to the file location (locate your pypcd.py  file) at,
\
 */venv/lib/python3.8/site-packages/pypcd/pypcd.py* \
remove,
```bash
from StringIO import StringIO
```
and replace with,
```bash
try:
    from StringIO import StringIO, BytesIO
except ImportError:
    from io import BytesIO, StringIO
```
## Usage
The PCD file is in binary format with XYZI information. 
### Run
```bash
git clone https://github.com/khalisfadil/Autobin-pcd2bin-converter.git
```
In file folder there are an example of file in each designated categories. Delete them all and put all the PCD files in *raw_pcd* directory
then run the scripts,
```bash
python3 pcd2bin.py
```
your PCD files will be converted into 4 different format:
1. In *raw_pcd* directory - the intial PCD file Autobin which is in binary format
2. In *ascii_pcd* directory - the PCD binary format is converted to ASCII format
3. In *txt* directory - the PCD file is converted into .txt format
4. In *bin* directory - the txt files are readed, remove the header and convert into bin format
5. In *inside-.pcd.bin* - this is to read the binary data and to make sure it is readed correctly.
because our PCD data have 4 information which are XYZI. The binary data is readed and arrange into a array matrix with [*,4] size. 

If your PCD files have ring information IYZIR:

change the array size in line *92* in *pcd2bin.py* from
```bash
array = np.reshape(data, [num, 4])
```
into,
```bash
array = np.reshape(data, [num, 5])
```

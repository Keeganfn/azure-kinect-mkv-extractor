### Azure-kinect-mkv-extractor
Used to extract pointclouds, depth, ir, camera information, color, imu and transformations from a recorded azure connect mkv file. Built off of the python wrapper for the azure sdk Pyk4a: https://github.com/etiennedub/pyk4a. Requires you to have the Azure SDK already installed.

### Install Prerequisites
##### Azure Specific
Azure SDK: https://github.com/microsoft/Azure-Kinect-Sensor-SDK

Pyk4a: https://github.com/etiennedub/pyk4a

##### Python
Open3d, Opencv, Numpy

```pip3 install open3d numpy opencv-python```


### Example Usage
1. Simplest way to get all the data from every frame of a mkv:
``` python3 extract.py -a vid_dir/test_vid.mkv extraction_folder ```

2. Extracts the pointcloud, color frames and camera calibration from test_vid.mkv and saves it to the extraction folder:
``` python3 extract.py -p -c -cc vid_dir/test_vid.mkv extraction_folder ```

3. Same as above but starts at 3.5s mark and ends at the 5.5s mark:
``` python3 extract.py -p -c -cc --start 3.5 --stop 5.5 vid_dir/test_vid.mkv extraction_folder ```

4. Extracts the colorized depth images with a clipping range of 0 to 1500 from test_vid.mkv and saves it to the extraction folder:
``` python3 extract.py -dcol -cr 0 1500 vid_dir/test_vid.mkv extraction_folder ```


For a full list of optional arguments use the help flag: ```python3 extract.py -h```

### All optional arguments / Extractable Data
- ```"-s", "--start"```: Sets starting position in seconds. Default=0.0

- ```"-e", "--stop"```: Sets ending position in seconds. Default=EOF

- ```"-d", "--depth"```: Optional flag to save depth mask data.

- ```"-p", "--pointcloud"```: Optional flag to save pointcloud data from depth image transformed to color image space.

- ```"-c", "--color"```: Optional flag to save color image data.

- ```"-imu", "--imu"```: Optional flag to save imu data.

- ```"-ir", "--ir"```: Optional flag to save ir data.

- ```"-ctd", "--color_to_depth"```: Optional flag to save color image transformed to depth image space

- ```"-dtc", "--depth_to_color"```: Optional flag to save depth image transformed to color image space

- ```"-dtp", "--depth_to_point"```: Optional flag to save depth image transformed to a pointcloud without transforming it to color image space first.

- ```"-itc", "--ir_to_color"```: Optional flag to save ir image transformed to color image space.

- ```"-dcol", "--depth_colorized"```: Optional flag to save colorized depth image (visualization purposes).

- ```"-cr", "--clipping_range"```: Optional values to set the clipping range for the colorized depth image. Default=0, 5000

- ```"-cc", "--camera_calibration"```: Optional flag to save all camera calibration parameters.

- ```"-a", "--all"```: Optional flag to save all possible data.

  ###### Required Arguments
- ```"MKV_PATH"```: Path to Azure MKV file.
- ```"OUTPUT_PATH"```: Path to output directory (ie: path/to/dir/extraction_folder )



import numpy as np
import cv2
from argparse import ArgumentParser
import open3d

import pyk4a
from pyk4a import PyK4APlayback
from pyk4a import Config, PyK4A, transformation


def convert_to_bgra(color_image):
    color_image = cv2.imdecode(color_image, cv2.IMREAD_COLOR)
    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2RGBA)
    return color_image

def save_pointcloud(capture, calibration, path, frame):
    complete_path = path + "pointcloud_" + str(frame) + ".ply"

    # Convert color and get points and colors for the image
    color_converted = convert_to_bgra(capture.color)
    points = capture.depth_point_cloud.reshape((-1,3))
    colors = transformation.color_image_to_depth_camera(color_converted, capture.depth, calibration, True)[:,:,:3].reshape((-1, 3))
    # Create pointcloud using open3d
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(points)
    # Normalize colors
    pcd.colors = open3d.utility.Vector3dVector(colors.astype(float) / 255.0)
    # Save as .ply file
    open3d.io.write_point_cloud(complete_path, pcd)


def save_depth_raw(capture, calibration, path, frame):
    complete_path = path + "depth_raw_" + str(frame) + ".jpg"
    cv2.imwrite(complete_path, capture.depth)    


def save_color_raw(capture, calibration, path, frame):
    complete_path = path + "color_raw_" + str(frame) + ".jpg"
    cv2.imwrite(complete_path, capture.color)    

def save_ir(capture, path, frame):
    complete_path = path + "ir_raw_" + str(frame) + ".jpg"
    cv2.imwrite(complete_path, capture.ir)

def save_imu(capture, calibration, path, frame):
    pass

def save_color_to_depth(capture, calibration, path, frame):
    pass

def save_depth_to_color(capture, calibration, path, frame):
    pass

def save_depth_to_point(capture, calibration, path, frame):
    pass

def save_depth_colorized(capture, calibration, path, frame):
    pass

#This is a very sloppy way to do this but it works fine for now 
def init_directories(depth_flag, pointcloud_flag, color_flag, imu_flag, ir_flag, 
                     color_to_depth_flag, depth_to_color_flag, depth_to_point_flag, depth_colorized_flag, all_flag, output_dir):
    if depth_flag or all_flag:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        pass
    if color_flag or all_flag:
        pass
    if pointcloud_flag or all_flag:
        pass
    if imu_flag or all_flag:
        pass
    if ir_flag or all_flag:
        pass
    if color_to_depth_flag or all_flag:
        pass
    if depth_to_color_flag or all_flag:
        pass
    if depth_to_point_flag or all_flag:
        pass
    if depth_colorized_flag or all_flag:
        pass

def main():
    # Setup arg parser
    parser = ArgumentParser(prog="AzureExtractor", 
                            description="Takes a pre-recorded azure .mkv file and extracts pointcloud, depth data, imu, ir and camera calibration for each frame. Uses the pyk4a package.")
    # All optional arguments
    parser.add_argument("-s", "--start", type=float, help="Sets starting position in seconds.", default=0.0)
    parser.add_argument("-e", "--stop", type=float, help="Sets ending position in seconds.", default=None)
    parser.add_argument("-d", "--depth", help="Optional flag to save depth mask data.", action="store_true")
    parser.add_argument("-p", "--pointcloud", help="Optional flag to save pointcloud data.", action="store_true")
    parser.add_argument("-c", "--color", help="Optional flag to save color image data.", action="store_true")
    parser.add_argument("-imu", "--imu", help="Optional flag to save imu data.", action="store_true")
    parser.add_argument("-ir", "--ir", help="Optional flag to save ir data.", action="store_true")
    parser.add_argument("-ctd", "--color_to_depth", help="Optional flag to save color image transformed to depth image space", action="store_true")
    parser.add_argument("-dtc", "--depth_to_color", help="Optional flag to save depth image transformed to color image space", action="store_true")
    parser.add_argument("-dtp", "--depth_to_point", help="Optional flag to save depth color image transformed to a pointcloud.", action="store_true")
    #TODO: ADD TRANSFORMED IR
    parser.add_argument("-dcol", "--depth_colorized", help="Optional flag to save colorized depth image", action="store_true")
    parser.add_argument("-a", "--all", help="Optional flag to save every extracted element.", action="store_true")

    # Required Arguments
    parser.add_argument("MKV_PATH", type=str, help="Path to MKV file written by k4arecorder.")
    parser.add_argument("OUTPUT_PATH", type=str, help="Path to output directory.")

    # Save parsed args
    args = parser.parse_args()
    mkv: str = args.MKV_PATH
    output_dir: str = args.OUTPUT_PATH
    start_time: float = args.start
    stop_time: float = args.stop   
    depth_flag: bool = args.depth
    pointcloud_flag: bool = args.pointcloud
    color_flag: bool = args.color
    imu_flag: bool = args.imu
    ir_flag: bool = args.ir
    color_to_depth_flag: bool = args.color_to_depth
    depth_to_color_flag: bool = args.depth_to_color
    depth_to_point_flag: bool = args.depth_to_point
    depth_colorized_flag: bool = args.depth_colorized
    all_flag: bool = args.all

    # Open up playback
    playback = PyK4APlayback(mkv)
    playback.open()
    # Seek if needed to desired start time (microseconds)
    if start_time != 0.0:
        playback.seek(int(start_time * 1000000))

    # Set end timestamp if provided
    end_timestamp = None
    if stop_time != None:
        end_timestamp = int(stop_time * 1000000)

    frame = 0
    # Loops until EOF or optional end timestamp
    while True:
        try:
            break
            # Get next capture and check that we are not at end timestamp if one is provided
            capture = playback.get_next_capture()
            frame += 1
            if end_timestamp != None and capture.color_timestamp_usec >= end_timestamp: 
                break
            # Only process if we have depth and color
            if capture.color is not None and capture.depth is not None:
                if depth_flag or all_flag:
                    pass
                    #save_depth_raw()
                if color_flag or all_flag:
                    pass
                    #save_color_raw()
                if pointcloud_flag or all_flag:
                    save_pointcloud(capture, playback.calibration, output_dir, frame)
                if imu_flag or all_flag:
                    pass
                    #save_imu()
                if ir_flag or all_flag:
                    save_ir(capture, output_dir, frame)
                if color_to_depth_flag or all_flag:
                    pass
                    #save_color_to_depth()
                if depth_to_color_flag or all_flag:
                    pass
                    #save_depth_to_color()
                if depth_to_point_flag or all_flag:
                    pass
                    #save_depth_to_point()
                if depth_colorized_flag or all_flag:
                    pass
                    #save_depth_colorized()
        except EOFError:
            break

    # Cleanup playback
    playback.close()
 
if __name__ == "__main__":
    main()
    print("HERE")
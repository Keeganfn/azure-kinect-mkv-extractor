import numpy as np
import cv2
from argparse import ArgumentParser
from typing import Optional, Tuple
import csv
import open3d
import os
import shutil
import json
from pyk4a import PyK4APlayback, transformation
import signal
import sys

def handle_sigint(signal, frame):
    print("Interrupted. Exiting...")
    sys.exit(0)

# Taken from pyk4a examples: https://github.com/etiennedub/pyk4a/blob/master/example/helpers.py
def colorize(
        image: np.ndarray,
        clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
        colormap: int = cv2.COLORMAP_HSV,
) -> np.ndarray:
    if clipping_range[0] or clipping_range[1]:
        img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
    else:
        img = image.copy()
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img = cv2.applyColorMap(img, colormap)
    return img


def convert_to_bgra(color_image):
    color_image = cv2.imdecode(color_image, cv2.IMREAD_COLOR)
    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2RGBA)
    return color_image


def save_pointcloud(capture, calibration, path, frame):
    complete_path = os.path.join(path, "pointcloud/pointcloud_" + str(frame) + ".ply")

    # Convert color and get points and colors for the image
    color_converted = convert_to_bgra(capture.color)
    # points = capture.depth_point_cloud.reshape((-1, 3))
    points = capture.depth_point_cloud.reshape((-1, 3)).astype(np.float32)

    colors = transformation.color_image_to_depth_camera(color_converted, capture.depth, calibration, True)[:, :,
             :3].reshape((-1, 3))
    # Create pointcloud using open3d
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(points)
    # Normalize colors
    pcd.colors = open3d.utility.Vector3dVector(colors.astype(float) / 255.0)
    # Save as .ply file
    open3d.io.write_point_cloud(complete_path, pcd)

def save_depth_raw(capture, path, frame):
    complete_path = os.path.join(path, "depth/depth_raw_" + str(frame) + ".png")
    cv2.imwrite(complete_path, capture.depth)


def save_color_raw(capture, path, frame):
    complete_path = os.path.join(path, "color/color_raw_" + str(frame) + ".png")
    cv2.imwrite(complete_path, convert_to_bgra(capture.color))


def save_ir_raw(capture, path, frame):
    complete_path = os.path.join(path, "ir/ir_raw_" + str(frame) + ".png")
    cv2.imwrite(complete_path, capture.ir)


def save_ir_to_color(capture, path, frame):
    complete_path = os.path.join(path, "ir_to_color/ir_to_color_" + str(frame) + ".png")
    cv2.imwrite(complete_path, capture.transformed_ir)


def save_imu(imu_data, path):
    imu_path = os.path.join(path, "imu/imu_data.csv")
    with open(imu_path, "a", newline="") as csvfile:
        imu_writer = csv.writer(csvfile, delimiter=",")
        imu_writer.writerow(
            [imu_data["temperature"], imu_data["acc_sample"][0], imu_data["acc_sample"][1], imu_data["acc_sample"][2],
             imu_data["acc_timestamp"], imu_data["gyro_sample"][0], imu_data["gyro_sample"][1],
             imu_data["gyro_sample"][2],
             imu_data["gyro_timestamp"]])


def save_color_to_depth(capture, calibration, path, frame):
    color_converted = convert_to_bgra(capture.color)
    # transform to depth
    colors_transformed = transformation.color_image_to_depth_camera(color_converted, capture.depth, calibration, True)
    complete_path = os.path.join(path, "color_to_depth/color_to_depth_" + str(frame) + ".png")
    cv2.imwrite(complete_path, colors_transformed)


def save_depth_to_color(capture, path, frame):
    complete_path = os.path.join(path, "depth_to_color/depth_to_color_" + str(frame) + ".png")
    cv2.imwrite(complete_path, capture.transformed_depth)


def save_depth_to_point(capture, path, frame):
    complete_path = os.path.join(path, "depth_to_point/depth_to_point_" + str(frame) + ".ply")
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(capture.depth_point_cloud.reshape((-1, 3)))
    # Save as .ply file
    open3d.io.write_point_cloud(complete_path, pcd)


def save_depth_colorized(capture, calibration, path, frame, clipping_range):
    transformed_depth = transformation.depth_image_to_color_camera(capture.depth, calibration, True)
    complete_path = os.path.join(path, "depth_colorized/depth_colorized_" + str(frame) + ".png")
    cv2.imwrite(complete_path, colorize(transformed_depth, clipping_range=clipping_range))


def save_camera_calibration(playback, path):
    # TODO: Find  easy format for extrinsics
    calib_dict = {}
    calib_dict["color_intrinsic"] = list(playback.calibration.get_camera_matrix(1).flatten())
    calib_dict["color_distortion_coef"] = list(playback.calibration.get_distortion_coefficients(1).flatten())
    # calib_dict["color_extrinsic_to_depth"] = list(playback.calibration.get_extrinsic_parameters(1,0).flatten())

    calib_dict["depth_intrinsic"] = list(playback.calibration.get_camera_matrix(0).flatten())
    calib_dict["depth_distortion_coef"] = list(playback.calibration.get_distortion_coefficients(0).flatten())
    # calib_dict["depth_extrinsic_to_color"] = list(playback.calibration.get_extrinsic_parameters(0,1).flatten())

    complete_path = os.path.join(path, "camera_calibration/camera_calibration.json")
    with open(complete_path, 'w', encoding='utf-8') as f:
        json.dump(calib_dict, f, ensure_ascii=False, indent=4)


def init_directories(dir_names, output_dir):
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir)

    # Creates all needed sub directories
    for i in dir_names:
        full_path = output_dir + "/" + i
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
        os.makedirs(full_path)
        if i == "imu":
            imu_path = os.path.join(full_path, "imu_data.csv")
            with open(imu_path, "w", newline="") as csvfile:
                imu_writer = csv.writer(csvfile, delimiter=",")
                imu_writer.writerow(["temperature", "acc_sample_x", "acc_sample_y", "acc_sample_z",
                                     "acc_timestamp", "gyro_sample_x", "gyro_sample_y", "gyro_sample_z",
                                     "gyro_timestamp"])


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Setup arg parser
    parser = ArgumentParser(prog="AzureExtractor",
                            description="Takes a pre-recorded azure .mkv file and extracts pointcloud, depth data, imu, ir and camera calibration for each frame. Uses the pyk4a package.")
    # All optional arguments
    parser.add_argument("-s", "--start", type=float, help="Sets starting position in seconds.", default=0.0)
    parser.add_argument("-e", "--stop", type=float, help="Sets ending position in seconds.", default=None)
    parser.add_argument("-d", "--depth", help="Optional flag to save depth mask data.", action="store_const",
                        const="depth", default=None)
    parser.add_argument("-p", "--pointcloud",
                        help="Optional flag to save pointcloud data from depth image transformed to color image space",
                        action="store_const", const="pointcloud", default=None)
    parser.add_argument("-c", "--color", help="Optional flag to save color image data.", action="store_const",
                        const="color", default=None)
    parser.add_argument("-imu", "--imu", help="Optional flag to save imu data.", action="store_const", const="imu",
                        default=None)
    parser.add_argument("-ir", "--ir", help="Optional flag to save ir data.", action="store_const", const="ir",
                        default=None)
    parser.add_argument("-ctd", "--color_to_depth",
                        help="Optional flag to save color image transformed to depth image space", action="store_const",
                        const="color_to_depth", default=None)
    parser.add_argument("-dtc", "--depth_to_color",
                        help="Optional flag to save depth image transformed to color image space", action="store_const",
                        const="depth_to_color", default=None)
    parser.add_argument("-dtp", "--depth_to_point",
                        help="Optional flag to save depth image transformed to a pointcloud without transforming it to color image space first.",
                        action="store_const", const="depth_to_point", default=None)
    parser.add_argument("-itc", "--ir_to_color", help="Optional flag to save ir image transformed to color image space",
                        action="store_const", const="ir_to_color", default=None)
    parser.add_argument("-dcol", "--depth_colorized",
                        help="Optional flag to save colorized depth image (visualization purposes)",
                        action="store_const", const="depth_colorized", default=None)
    parser.add_argument("-cr", "--clipping_range", nargs=2, type=int,
                        help="Optional flag to set the clipping range for colorized depth image (default is 0-5000)",
                        default=(0, 5000))
    parser.add_argument("-cc", "--camera_calibration", help="Optional flag to save all camera calibration parameters.",
                        action="store_const", const="camera_calibration", default=None)
    parser.add_argument("-a", "--all", help="Optional flag to save every extracted element.", action="store_true")
    # Required Arguments
    parser.add_argument("MKV_PATH", type=str, help="Path to MKV file written by k4arecorder.")
    parser.add_argument("OUTPUT_PATH", type=str, help="Path to output directory (ie: path/to/dir/extraction_folder )")

    # Save parsed args
    args = parser.parse_args()
    mkv: str = args.MKV_PATH
    output_dir: str = args.OUTPUT_PATH
    start_time: float = args.start
    stop_time: float = args.stop
    all_flag: bool = args.all

    # Initialize the needed directories based on arguments
    if all_flag:
        init_directories(["depth", "color", "pointcloud", "imu", "ir",
                          "color_to_depth", "depth_to_color", "depth_to_point",
                          "ir_to_color", "depth_colorized", "ir_to_color",
                          "camera_calibration", "imu"], output_dir=output_dir)
    else:
        names = [i for i in vars(args).values() if i is not None and isinstance(i, str)][:-2]
        print(names)
        init_directories(names, output_dir=output_dir)

    # Open up playback
    playback = PyK4APlayback(mkv)
    playback.open()
    # Seek if needed to desired start time (microseconds)
    if start_time != 0.0:
        playback.seek(int(start_time * 1000000))

    if args.camera_calibration or all_flag:
        save_camera_calibration(playback, output_dir)

    # Set end timestamp if provided
    end_timestamp = None
    if stop_time != None:
        end_timestamp = int(stop_time * 1000000)
    frame = 0
    # Loops until EOF or optional end timestamp
    while True:
        try:
            # Get next capture and check that we are not at end timestamp if one is provided
            capture = playback.get_next_capture()
            imu = playback.get_next_imu_sample()

            frame += 1
            if end_timestamp != None and capture.color_timestamp_usec >= end_timestamp:
                break
            # Only process if we have depth and color
            if capture.color is not None and capture.depth is not None:
                if args.depth or all_flag:
                    save_depth_raw(capture, output_dir, frame)
                if args.color or all_flag:
                    save_color_raw(capture, output_dir, frame)
                if args.pointcloud or all_flag:
                    save_pointcloud(capture, playback.calibration, output_dir, frame)
                if args.imu or all_flag:
                    save_imu(imu, output_dir)
                if args.ir or all_flag:
                    save_ir_raw(capture, output_dir, frame)
                if args.color_to_depth or all_flag:
                    save_color_to_depth(capture, playback.calibration, output_dir, frame)
                if args.depth_to_color or all_flag:
                    save_depth_to_color(capture, output_dir, frame)
                if args.depth_to_point or all_flag:
                    save_depth_to_point(capture, output_dir, frame)
                if args.depth_colorized or all_flag:
                    save_depth_colorized(capture, playback.calibration, output_dir, frame, args.clipping_range)
                if args.ir_to_color or all_flag:
                    save_ir_to_color(capture, output_dir, frame)
        except EOFError:
            break

    # Cleanup playback
    playback.close()


if __name__ == "__main__":
    main()
    print("COMPLETE")
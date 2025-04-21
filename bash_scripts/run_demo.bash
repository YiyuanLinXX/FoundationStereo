python ../scripts/run_demo.py --left_file ../datasets/Crittenden_1004/left/00115_016E9093.png --right_file ../datasets/Crittenden_1004/right/00115_016F4E63.png --out_dir ../outputs/Crittenden_1004_00115 --scale 0.25


# usage: run_demo.py [-h] [--left_file LEFT_FILE] [--right_file RIGHT_FILE] [--intrinsic_file INTRINSIC_FILE]
#                    [--ckpt_dir CKPT_DIR] [--out_dir OUT_DIR] [--scale SCALE] [--hiera HIERA] [--z_far Z_FAR]
#                    [--valid_iters VALID_ITERS] [--get_pc GET_PC] [--remove_invisible REMOVE_INVISIBLE]
#                    [--denoise_cloud DENOISE_CLOUD] [--denoise_nb_points DENOISE_NB_POINTS]
#                    [--denoise_radius DENOISE_RADIUS]

# optional arguments:
#   -h, --help            show this help message and exit
#   --left_file LEFT_FILE
#   --right_file RIGHT_FILE
#   --intrinsic_file INTRINSIC_FILE
#                         camera intrinsic matrix and baseline file
#   --ckpt_dir CKPT_DIR   pretrained model path
#   --out_dir OUT_DIR     the directory to save results
#   --scale SCALE         downsize the image by scale, must be <=1
#   --hiera HIERA         hierarchical inference (only needed for high-resolution images (>1K))
#   --z_far Z_FAR         max depth to clip in point cloud
#   --valid_iters VALID_ITERS
#                         number of flow-field updates during forward pass
#   --get_pc GET_PC       save point cloud output
#   --remove_invisible REMOVE_INVISIBLE
#                         remove non-overlapping observations between left and right images from point cloud, so the
#                         remaining points are more reliable
#   --denoise_cloud DENOISE_CLOUD
#                         whether to denoise the point cloud
#   --denoise_nb_points DENOISE_NB_POINTS
#                         number of points to consider for radius outlier removal
#   --denoise_radius DENOISE_RADIUS
#                         radius to use for outlier removal
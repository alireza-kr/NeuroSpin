#!/bin/bash

# $1, $2, $3, ... are the variables that will be passed by Python code (by order of passing)

# root_path: The target path where exp_info folder is within this path
# dataset_name: Folder where bids converted data will be saved
# acquisition_dir: Acquisition folder of Neurospin (/neurospin/acquisition)
# noninteractive: Deface after preprocessing

neurospin_to_bids \
    --root-path $1 \
    --dataset-name  $2 \
    --acquisition-dir $3 \
    --noninteractive
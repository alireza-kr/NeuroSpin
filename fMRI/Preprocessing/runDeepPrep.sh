#!/bin/bash

export SOURCE=$1
export DEST=$2
export SUBJ=$3

singularity run --cleanenv --nv \
             -B ${SOURCE}:/input \
             -B ${DEST}:/output \
             -B /data/software/fmriprep/fs_license.txt:/fs_license.txt \
             /data/software/deepprep/deepprep_25.1.0.sif \
             /input \
             /output \
             participant \
             --fs_license_file /fs_license.txt \
             --participant_label ${SUBJ} \
             --bold_task_type [YOUR TASKS] \
             --bold_volume_space MNI152NLin2009cAsym \
             --bold_volume_res 02 \
             --bold_surface_spaces 'fsaverage6' 'fsnative' \
             --cifti-output \
             --skip_bids_validation \
	     --ignore_error \
             --device gpu

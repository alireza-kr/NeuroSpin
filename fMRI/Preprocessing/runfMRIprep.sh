#!/bin/bash

export FMRIPREP=/neurospin/unicog/resources/softwares/FMRIPREP/fmriprep-22.0.2.simg
export FREESURFER=$FREESURFER_HOME
export PROJECT=$1
export SOURCE=$2
export DEST=$3
export SUBJ=$4

singularity run --cleanenv \
            -B "${PROJECT}:/data" \
            -B "${FREESURFER}:/freesurfer" \
            ${FMRIPREP} \
            "/data/${SOURCE}" \
            "/data/${DEST}" \
            participant \
                --participant-label ${SUBJ} \
                --output-spaces T1w MNI152NLin2009cAsym \
                --bold2t1w-init header \
                --bold2t1w-dof 9 \
                --fs-license-file "/freesurfer/license.txt" \
                --work-dir "/data/${DEST}/work_dir" \
                --skip-bids-validation \
                --clean-workdir

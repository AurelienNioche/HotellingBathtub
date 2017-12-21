#!/bin/bash

N_JOBS=$(eval python avakas/count_jobs.py)
N_JOBS_MINUS_1=$(($N_JOBS - 1))
INDICES="0-${N_JOBS_MINUS_1}"

# qsub needs Python 2 on the avakas cluster
export PYENV_VERSION=2.7.12

CMD="qsub -t ${INDICES} avakas/job_array.pbs"
echo $CMD >> avakas/job_names.txt
eval $CMD

unset PYENV_VERSION

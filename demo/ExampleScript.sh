#!/usr/bin/env bash

set -e
PATH=$PATH:/some/tool
PYTHONPATH=$PYTHONPATH:/python/path
1. precommand
2. precommand
/Users/ttickle/Documents/safe/dev/SciEDPipeR/ExampleScript.sh --threads 0 --jobs_file None --test --compress none --pipeline_config_file None --out_dir /Users/ttickle/Documents/safe/dev/SciEDPipeR --wait 5,15,40 --wdl True --update_command None --sample_file None --timestamp 0.0 --sample_name sample name --copy None --log new_log --resources ExampleScript.resource.config --move None --concurrent_jobs 1 --file_one file one --bsub_queue new_bsub_queue --file_two file two --example some_reference.fasta --json_out True --max_bsub_memory 11 --no_pipeline_config
1. postcommand
2. postcommand
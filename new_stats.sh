#!/bin/bash

# Define checkpoints directory
CHECKPOINTS_DIR=/Users/bharathsurianarayanan/Desktop/gymjam/lander_steps_output
PREV_RUN_CHECKPOINTS_DIR=/Users/bharathsurianarayanan/Desktop/gymjam/lander_steps_output
RESULTS_DIR=/Users/bharathsurianarayanan/Desktop/gymjam/lander_steps_stats

# Lisa runs files
CHECKPOINTS_DIR_LISA=../gymjam_results/lisa_results/mortality
CHECKPOINTS_DIR_LISA2=../gymjam_results/lisa_results/scaling

# Create aggregations file
AGGS_FILE=aggregations.csv
echo "file_name,best_fitness,best_fitnesss_mean,best_fitness_std,best_fitness_times_mean,best_fitness_times_std,summed_fitness_mean,summed_fitness_std,cells_filled_mean,cells_filled_std" > $AGGS_FILE
#
## Experiment 1
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment01_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e01* \
#    --outFile="exp01_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 2
#python checkpoint-printer.py \
#    --files $PREV_RUN_CHECKPOINTS_DIR/experiment02_*_latest.pkl \
#    --outFile="exp02_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 2.1 - Slurm File -- results file unavailable, parsing logs
#python parse-slurm-files.py \
#    --files ../gymjam_results/2020_04_22_experiments/logfiles/*_e02*.out \
#    --outFile=exp02_stats
#
## Experiment 3
#python checkpoint-printer.py \
#    --files $PREV_RUN_CHECKPOINTS_DIR/experiment03_*_latest.pkl \
#    --outFile="exp03_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 3.1 - Slurm File -- results file unavailable, parsing logs
#python parse-slurm-files.py \
#    --files ../gymjam_results/2020_04_22_experiments/logfiles/*_e03*.out \
#    --outFile=exp03_stats
#
## Experiment 4
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment04_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e04* \
#    --outFile="exp04_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 5
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment05_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e05* \
#    --outFile="exp05_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 6
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment06_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e06* \
#    --outFile="exp06_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 7
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment07_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e07* \
#    --outFile="exp07_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 8
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment08_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e08* \
#    --outFile="exp08_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 9
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment09_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e09* \
#    --outFile="exp09_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 10
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR_LISA/endpoint/checkpoints/experiment06_*_latest.pkl \
#    --result-files $CHECKPOINTS_DIR_LISA/endpoint/results0.txt \
#    --outFile="exp10_stats" \
#    --aggregations=$AGGS_FILE

## Experiment 11
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR_LISA/polyhash/checkpoints/experiment07_*_latest.pkl \
#    --result-files $CHECKPOINTS_DIR_LISA/polyhash/results0.txt \
#    --outFile="exp11_stats" \
#    --aggregations=$AGGS_FILE
##
## Experiment 12
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR_LISA/fitness/checkpoints/experiment08_*_latest.pkl \
#    --result-files $CHECKPOINTS_DIR_LISA/fitness/results0.txt \
#    --outFile="exp12_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 13
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR_LISA/entropy/checkpoints/experiment09_*_latest.pkl \
#    --result-files $CHECKPOINTS_DIR_LISA/entropy/results0.txt \
#    --outFile="exp13_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 14
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment14_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e14* \
#    --outFile="exp14_stats" \
#    --aggregations=$AGGS_FILE
#
## Experiment 15
#python checkpoint-printer.py \
#    --files $CHECKPOINTS_DIR/experiment09_*_latest.pkl \
#    --result-files $RESULTS_DIR/results_e15* \
#    --outFile="exp15_stats" \
#    --aggregations=$AGGS_FILE

# Experiment 16
# lander steps difference
# landerStepsDiff_20_latest.pkl
python3.7 checkpoint-printer.py \
    --files $CHECKPOINTS_DIR/landerStepsDiff_*_latest.pkl \
    --outFile="lander_steps_exp1_stats" \
    --aggregations=$AGGS_FILE

# Experiment 17
# python checkpoint-printer.py \
#     --files $CHECKPOINTS_DIR_LISA2/entropy/checkpoints/experiment09_*_latest.pkl \
#     --result-files $CHECKPOINTS_DIR_LISA2/entropy/results0.txt \
#     --outFile="exp17_stats" \
#     --aggregations=$AGGS_FILE
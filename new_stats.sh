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

python3.7 checkpoint-printer.py \
    --files $CHECKPOINTS_DIR/landerStepsDiff_*_latest.pkl \
    --outFile="lander_steps_exp1_stats" \
    --aggregations=$AGGS_FILE


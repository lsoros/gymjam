#!/bin/sh
#
#SBATCH --verbose
#SBATCH --job-name=lunE14
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --mem=1GB

# /bin/hostname
# /bin/pwd

# #module load python3/intel/3.6.3

# eval "$(pyenv init -)"
# pyenv activate lunarlander

# Where results are going to be written
# OUTDIR=/scratch/od356/lunarlander_experiments_03
# Make changes to this OUTDIR as required
OUTDIR=/Users/bharathsurianarayanan/Desktop/gymjam/lander_angle_stats

# /Users/bharathsurianarayanan/Desktop/gymjam/lander_steps_output
# /Users/bharathsurianarayanan/Dropbox/My Mac (Bharath’s MacBook Pro)/Desktop/gymjam
CHECKPOINT_FREQ=100

#NUM_INDIVIDUALS=1000 #test run
NUM_INDIVIDUALS=100000 #real experiment
SIZER_RANGE=200

for n in {19..20}
do
    python lander_angle_and_velocity.py \
           --sizer-range 2 200 \
           --run-id=ME_lander_angle_velocityBC_scaling_$n \
           --search-type=ME \
           --mode='ME-angleVelocityBC' \
           --init-population-size=1000 \
           --num-individuals=$NUM_INDIVIDUALS \
           --checkpoint-dir=$OUTDIR \
           --checkpoint-prefix=ME_lander_angle_velocityBC_scaling_$n \
           --checkpoint-enabled \
           --checkpoint-frequency=$CHECKPOINT_FREQ \
           --seed=1008
done
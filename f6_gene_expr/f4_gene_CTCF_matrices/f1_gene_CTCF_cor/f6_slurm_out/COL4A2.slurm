#!/bin/bash

#SBATCH -n 1
#SBATCH --mem=4000
#SBATCH -t 24:00:00
#SBATCH -p standard
#SBATCH -A zanglab
#SBATCH -o COL4A2.out

time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A2 
time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A3 
time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A3BP 
time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A4 
time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A5 
time python ../7_cor_CTCF_binding_GeneExpr.py -i COL4A6 

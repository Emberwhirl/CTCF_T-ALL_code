#!/bin/bash

#SBATCH -n 1
#SBATCH --mem=4000
#SBATCH -t 24:00:00
#SBATCH -p standard
#SBATCH -A zanglab
#SBATCH -o POM121L2.out

time python ../7_cor_CTCF_binding_GeneExpr.py -i POM121L2 
time python ../7_cor_CTCF_binding_GeneExpr.py -i POM121L4P 
time python ../7_cor_CTCF_binding_GeneExpr.py -i POM121L8P 
time python ../7_cor_CTCF_binding_GeneExpr.py -i POM121L9P 
time python ../7_cor_CTCF_binding_GeneExpr.py -i POMC 
time python ../7_cor_CTCF_binding_GeneExpr.py -i POMGNT1 

#!/bin/bash

#SBATCH -n 1
#SBATCH --mem=4000
#SBATCH -t 24:00:00
#SBATCH -p standard
#SBATCH -A zanglab
#SBATCH -o KLK15.out

time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK15 
time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK2 
time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK3 
time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK4 
time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK5 
time python ../7_cor_CTCF_binding_GeneExpr.py -i KLK6 

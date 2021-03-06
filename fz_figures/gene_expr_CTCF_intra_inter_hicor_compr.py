'''
This is used to plot the distribution of distances from gene-CTCF pair that
with R-squared values higher than a threshold
'''

import sys,argparse
import os,glob
import numpy as np
import pandas as pd
#from GenomeData import *
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.size']=16
matplotlib.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "Bitstream Vera Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
# import seaborn as sns
# sns.set(font_scale=2)
# sns.set_style("whitegrid", {'axes.grid' : False})
import random

chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']

def plot_plt_ax2(x,plot_lists,plot_labels,figname):
    
    fig,ax1 = plt.subplots(figsize=(4.5,3.7))
    b = ax1.plot(x,plot_lists[1],label = plot_labels[1],color = 'grey',linewidth=3)
    a = ax1.plot(x,plot_lists[0],label = plot_labels[0],color = 'navy',linewidth=3)
    ax1.set_ylabel('% $R^2$ > 0.25',fontsize=20)
    ax1.set_ylim([1,12.5])
    
    ax2 = ax1.twinx()
    c = ax2.plot(x,plot_lists[2],label = plot_labels[2],color = 'coral',linewidth=3)
    ax2.set_ylabel('-log10 $p$',fontsize=20)
    ax2.set_yscale('log')
    ax2.axhline(y=-np.log10(0.05),color='k',linestyle='--',linewidth=1)
    ax2.set_ylim([1,1000])
    ls = a+b+c
    labs = [l.get_label() for l in ls]
    ax1.legend(ls,labs,loc=2,bbox_to_anchor=[.2,1],fontsize=15,frameon=False,borderaxespad=0.2,labelspacing=.2,handletextpad=1,handlelength=1)
    ax1.set_xlabel('CTCF-gene pairwise distance',fontsize=20)
    plt.xscale('log')
    #plt.xlim([0,10000000])
    
    plt.savefig(figname,bbox_inches = 'tight',pad_inches = 0.1,transparent=True)
    plt.close()
   
   

def plot_by_indir(indir_name,indir):
    
    indir_sub='{}/{}'.format(indir,indir_name)
    outdir='figures/gene_expr_CTCF_intra_inter_hicor_compr/'
    os.makedirs(outdir,exist_ok=True)
    
    df = pd.DataFrame()
    for chrom in chroms:
        df_tmp = pd.read_csv(indir_sub+os.sep+'{}.csv'.format(chrom),index_col=0)
        if df.shape[0]==0:
            df = df_tmp
        elif df_tmp.shape[0]!=0:
            df = df+df_tmp
    
    #print(df);exit()
    #df.loc[[i for i in df.index if i<100000],['inter_all','inter_GT0.25']]=0
    #df.loc[[i for i in df.index if i>1000000],['intra_all', 'intra_GT0.25']]=0
    
    df.to_csv('{}/intra_inter_{}.csv'.format(outdir,indir_name))
    intra_plot,inter_plot,pvalue_plot,xticklabels  = [],[],[],[]
    
    a1,a2=4,35
    index_sep= np.append(df.index[:a1],df.index[a1:a2:5])
    index_sep= np.append(index_sep,df.index[a2::6])
    print(index_sep)
#     index_sep.to_csv('{}/intra_inter_{}_index_seq.csv'.format(outdir,indir_name))
    
    print('start','end','intra_GT0.25','intra_all','inter_GT0.25','inter_all','s','p')
    for index_start in np.arange(len(index_sep)-1):
        start = index_sep[index_start]
        end = index_sep[index_start+1]
        df_sep= df.loc[[i for i in df.index if i >=start and i<=end]].sum()
        a = df_sep['intra_GT0.25']# len([i for i in intra_domain_total[pos] if i >.25])
        b = df_sep['intra_all']#len(intra_domain_total[pos])
        c = df_sep['inter_GT0.25']#len([i for i in inter_domain_total[pos] if i >.25]) 
        d = df_sep['inter_all']#len(inter_domain_total[pos])
        #outfile.write('{}\t{}\t{}\t{}\t{}\n'.format(pos,a,b,c,d))     
        score,pvalue = stats.fisher_exact([[a,b-a],[c,d-c]])
        print('{:.0f}\t{:.0f}\t{}\t{}\t{}\t{}\t{:.1f}\t{:.2e}'.format(start,end,a,b,c,d,score,pvalue))
        intra_plot.append(100*a/b if b!=0 else 0)
        inter_plot.append(100*c/d if d!=0 else 0)
        pvalue_plot.append(-np.log(pvalue))
        xticklabels.append(start)
    #pvalue_plot = [0 if i==np.inf else i for i in pvalue_plot]
    #pvalue_plot = [max(pvalue_plot) if i==0 else i for i in pvalue_plot]
    plot_labels = ['Intra domain','Inter domain','p-value']
    plot_plt_ax2(xticklabels,[intra_plot,inter_plot,pvalue_plot],plot_labels,'{}/intra_inter_pvalue_{}.pdf'.format(outdir,indir_name))


def main():

    indir = '/nv/vol190/zanglab/zw5j/work2017/T_ALL_CTCF/updated_201906/f6_gene_expr/f5_gene_CTCF_cor_figs/genome_intra_inter_domain_cor_compr/f7_intra_inter_hicor_sep_chr_domain_NoLimit'
    name_lists = glob.glob('{}/sep*'.format(indir))
    name_lists = [os.path.basename(i) for i in name_lists]
#     print(name_lists);exit()
    for name_list in name_lists:  
        print(name_list)
        plot_by_indir(name_list,indir);#exit()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', action = 'store', type = str,dest = 'infile', help = 'input file of', metavar = '<file>')
    parser.add_argument('-o','--outfile', action = 'store', type = str,dest = 'outfile', help = 'outfile of', metavar = '<file>')
    #parser.add_argument('-i', '--indir', action = 'store', type = str,dest = 'indir', help = 'input dir of ', metavar = '<dir>')
    #parser.add_argument('-o','--outdir', action = 'store', type = str,dest = 'outdir', help = 'outdir of ,default: current dir', metavar = '<dir>',default='./')
    #parser.add_argument('-s','--species', action = 'store', type = str,dest = 'species', help = 'species used to choose correct chromosome, e.g., hg38 or mm10', metavar = '<str>',required=True)
    

    args = parser.parse_args()
    if(len(sys.argv))<0:
        parser.print_help()
        sys.exit(1)
  
    main()

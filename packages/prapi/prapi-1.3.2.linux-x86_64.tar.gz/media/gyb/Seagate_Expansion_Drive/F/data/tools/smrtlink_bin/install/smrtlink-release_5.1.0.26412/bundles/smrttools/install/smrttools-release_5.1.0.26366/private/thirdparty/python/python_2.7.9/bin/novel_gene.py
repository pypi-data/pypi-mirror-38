#!/media/gyb/Seagate_Expansion_Drive/F/data/tools/smrtlink_bin/install/smrtlink-release_5.1.0.26412/bundles/smrttools/install/smrttools-release_5.1.0.26366/private/thirdparty/python/python_2.7.9/bin/python
import os,sys,re
from  collections import defaultdict
########
cluster_file=sys.argv[1]
outdir=sys.argv[2]
Output_dir=sys.argv[3]
#########
if not os.path.exists(outdir):
	os.makedirs(outdir)
####
sys.stderr.write('Reading Cluster file...\n')
cluster=open(cluster_file,'r')
mapdict=defaultdict(dict)
for line in cluster:
	line=line.strip('\n')
	name=line.split()[0]
	mapdict[name][line]=1
sys.stderr.write('Reading  Pacbio Cluster file finshed...\n')
############
for i in mapdict:
	gene=i.split(';')[0]
	strand=list(set([x.split()[4] for x in mapdict[i]]))
	if len(strand)==2:
		continue
	strand=strand[0]
	#######################
	minpos  = min(int(x.split()[2]) for x in mapdict[i])
	maxpos  = max(int(x.split()[3]) for x in mapdict[i])
	minpos=int(minpos)
	maxpos=int(maxpos)
	Gene_coordinate="%s:%d-%d"%(gene,minpos,maxpos)
	#######################
	

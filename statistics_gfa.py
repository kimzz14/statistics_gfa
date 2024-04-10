#####################################################################################
def get_N(sortedLength_LIST, N):
    totalLength = sum(sortedLength_LIST)
    sumLength = 0
    for idx, length in enumerate(sortedLength_LIST):
        sumLength += length
        if float(sumLength) / totalLength > (float(N)/100):
            return length, idx
#####################################################################################
from optparse import OptionParser
import sys
#option parser
parser = OptionParser(usage="""Run annotation.py \n Usage: %prog [options]""")
parser.add_option("-i","--input",action = 'store',type = 'string',dest = 'INPUT',help = "")
(opt, args) = parser.parse_args()
if opt.INPUT == None:
    print('Basic usage')
    print('')
    print('     python statistics_gfa.py -i test.gfa')
    print('')
    sys.exit()

infile = opt.INPUT
fin = open(infile)
contigLength_LIST = []
for line in fin:
    if line[0] == 'S':
        mylist = line.rstrip('\n').split('\t')
        tag, contigName, contigSeq = line.rstrip('\n').split('\t')[0:3]
        contigLength = len(contigSeq)
        contigLength_LIST += [contigLength]
    else:
        pass

contigN = len(contigLength_LIST)
totalAssemblyLength = sum(contigLength_LIST)
minContigLength = min(contigLength_LIST)
maxContigLength = max(contigLength_LIST)

sortedContigLength_LIST = sorted(contigLength_LIST, reverse=True)

print('Number of contigs:' + '\t' + str(contigN))
print('Total assembly length:' + '\t' + str(totalAssemblyLength))
print('Min contig length:' + '\t' + str(minContigLength))
print('Max contig length:' + '\t' + str(maxContigLength))
print('Contig N50:' + '\t' + '\t'.join(get_N(sortedContigLength_LIST, 50)))
print('Contig N90:' + '\t' + '\t'.join(get_N(sortedContigLength_LIST, 90)))

import math

logCount_LIST = [0]*(int(math.log2(maxContigLength)) + 1)
logSum_LIST   = [0]*(int(math.log2(maxContigLength)) + 1)
for contigLength in sortedContigLength_LIST:
    logCountIDX = int(math.log2(contigLength))
    logCount_LIST[logCountIDX] += 1
    logSum_LIST[logCountIDX]   += contigLength

fout = open(infile + '.' + 'logCount', 'w')
for logCountIDX, (logCount, logSum) in enumerate(zip(logCount_LIST, logSum_LIST)):
    fout.write('\t'.join(map(str, [logCountIDX, logCount, logSum])) + '\n')
fout.close()
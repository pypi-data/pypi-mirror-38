#!/usr/bin/env python
#coding:utf-8
'''For sam to pairwise
Usage: sam2pairview queryseq cigarstring [md_tag]
    or sam2pairview bamfile|samfile
    or sam2pairview < samfile > out
'''

import sys,re,pysam
from itertools import chain,izip_longest
RED = re.compile("\D+")
REd = re.compile("\d+")

def get_pairwise(queryseq=None,cigar=None,md=None):
    ref,pair,query = "","",""
    delseq = []
    md_mis,mdp,pos,has_NP,X_len = {},0,1,0,0
    if md is not None:                        
        md_list = list(chain(*zip(re.split("\D+",md),re.split("\d+",md)[1:])))
        if md_list[-1] == "0":md_list.pop()
        for i in md_list:
            if i == "":
                continue
            try:
                mdp += int(i)
            except:
                if i.startswith("^"):
                    dseq = i.strip("^")
                    mdp += len(dseq)
                    delseq.extend(dseq)
                    # delseq.append(dseq)
                else:
                    mdp += 1
                    md_mis[mdp] = i                   
    if not cigar[0].isdigit():
        raise Exception, "Shift CIGAR failed, abnormal CIGAR string not startswith digit."
    cigarlist = re.findall("\D",cigar)  
    if "X" in cigarlist or "D" in cigarlist:
        if md is None:
            raise Exception, "'X' or 'D' encountered in CIGAR without MD tag"
    cigarcount = map(int,re.findall("\d+",cigar))                      
    if cigarlist[0] == "H":  ##pop first Hard Clip
        cigarlist.pop(0)
        cigarcount.pop(0)
    cigar_pos = [0,]
    c_pos = 0
    for n,i in enumerate(cigarcount):
        if cigarlist[n] not in ["N","P"]:
            c_pos += i
            cigar_pos.append(c_pos)       
    if delseq:
        delseq = iter(delseq)
        for n,c in enumerate(cigarlist):            
            if c == "D":                                
                queryseq = queryseq[:cigar_pos[n]] + "".join([delseq.next() for _ in range(cigarcount[n])]) + queryseq[cigar_pos[n]:]                        
                # queryseq = queryseq[:cigar_pos[n]] + delseq.next() + queryseq[cigar_pos[n]:]
    qseq = [queryseq[cigar_pos[i]:cigar_pos[i+1]] for i in range(len(cigar_pos)-1)]
    for n,t in enumerate(cigarlist):
        if t == "I":
            s = qseq[n-has_NP]
            ins = len(s)
            query += s                
            ref += "-"*ins
            pair += " "*ins
        elif t == "D":
            s = qseq[n-has_NP]
            dels = len(s)
            ref += s
            query += "-"*dels
            pair += " "*dels
            pos += dels
        elif t == "N":
            skip = cigarcount[n]
            ref += "N"*skip
            query += "."*skip
            pair += " "*skip
            has_NP += 1
        elif t == "M":
            s = qseq[n-has_NP]
            for p,base in enumerate(s):
                query += base                    
                if (pos + p) in md_mis:
                    ref += md_mis[pos + p].lower()
                    pair += " "
                else:
                    ref += base
                    pair += "|"
            pos += len(s) 
        elif t == "S":
            s = qseq[n-has_NP]
            query += s
            ref += "N"*len(s)
            pair += " "*len(s)
        elif t == "=":
            s = qseq[n-has_NP]
            query += s
            ref += s
            pair += "|"*len(s)
            pos += len(s)
        elif t == "X":
            s = qseq[n-has_NP]
            query += s
            ref += md_mis[pos-X_len].lower()
            pair += " "*len(s)
            pos += len(s)
            X_len += len(s) -1
        elif t == "P":
            has_NP += 1
            padding = cigarcount[n]
            ref += "*"*padding
            query += "*"*padding
            pair += " "*padding
        elif t == "H":
            continue
        else:
            raise Exception, "Unsupported CIGAR character encountered"    
    print "\n".join([ref+" (ref)",pair,query+" (query)"])
    
def get_pairwise2(rdaln):
    if rdaln.is_unmapped:
        print "unmapped read,(%s), failed."%rdaln.qname
        return
    ref,pair,query = "","",""
    delseq = []
    md_mis,mdp,pos,has_NP,X_len = {},0,1,0,0
    queryseq = rdaln.query_sequence
    md = None
    if rdaln.has_tag("MD"):
        md = rdaln.get_tag("MD")
        md_list = list(chain(*zip(re.split("\D+",md),re.split("\d+",md)[1:])))
        if md_list[-1] == "0":md_list.pop()
        for i in md_list:
            if i == "":
                continue
            try:
                mdp += int(i)
            except:
                if i.startswith("^"):
                    dseq = i.strip("^")
                    mdp += len(dseq)
                    delseq.extend(dseq)
                    # delseq.append(dseq)
                else:
                    mdp += 1
                    md_mis[mdp] = i 
    if not rdaln.cigarstring[0].isdigit():
        raise Exception, "shift_cigar failed."
    cigarlist = re.findall("\D",rdaln.cigarstring)  
    if "X" in cigarlist or "D" in cigarlist:
        if md is None:
            raise Exception, "'X' or 'D' encountered in CIGAR without MD tag"
    cigarcount = map(int,re.findall("\d+",rdaln.cigarstring))                      
    if cigarlist[0] == "H":  ##Hard Clip
        cigarlist.pop(0)
        cigarcount.pop(0)
    cigar_pos = [0,]
    c_pos = 0
    for n,i in enumerate(cigarcount):
        if cigarlist[n] not in ["N","P"]:
            c_pos += i
            cigar_pos.append(c_pos)       
    if delseq:
        delseq = iter(delseq)
        for n,c in enumerate(cigarlist):            
            if c == "D":                                
                queryseq = queryseq[:cigar_pos[n]] + "".join([delseq.next() for _ in range(cigarcount[n])]) + queryseq[cigar_pos[n]:]                        
                # queryseq = queryseq[:cigar_pos[n]] + delseq.next() + queryseq[cigar_pos[n]:]
    qseq = [queryseq[cigar_pos[i]:cigar_pos[i+1]] for i in range(len(cigar_pos)-1)]
    for n,t in enumerate(cigarlist):
        if t == "I":
            s = qseq[n-has_NP]
            ins = len(s)
            query += s                
            ref += "-"*ins
            pair += " "*ins
        elif t == "D":
            s = qseq[n-has_NP]
            dels = len(s)
            ref += s
            query += "-"*dels
            pair += " "*dels
            pos += dels
        elif t == "N":
            skip = cigarcount[n]
            ref += "N"*skip
            query += "."*skip
            pair += " "*skip
            has_NP += 1
        elif t == "M":
            s = qseq[n-has_NP]
            for p,base in enumerate(s):
                query += base                    
                if (pos + p) in md_mis:
                    ref += md_mis[pos + p].lower()
                    pair += " "
                else:
                    ref += base
                    pair += "|"
            pos += len(s) 
        elif t == "S":
            s = qseq[n-has_NP]
            query += s
            ref += "N"*len(s)
            pair += " "*len(s)
        elif t == "=":
            s = qseq[n-has_NP]
            query += s
            ref += s
            pair += "|"*len(s)
            pos += len(s)
        elif t == "X":
            s = qseq[n-has_NP]
            query += s
            ref += md_mis[pos-X_len].lower()
            pair += " "*len(s)
            pos += len(s)
            X_len += len(s) -1
        elif t == "P":
            has_NP += 1
            padding = cigarcount[n]
            ref += "*"*padding
            query += "*"*padding
            pair += " "*padding
        elif t == "H":
            continue            
        else:
            raise Exception, "Unsupported CIGAR character encountered"
    print "\t".join(map(str,[rdaln.query_name,rdaln.flag,rdaln.reference_name,rdaln.reference_start + 1,
        rdaln.mapping_quality,rdaln.cigarstring,rdaln.next_reference_name,rdaln.next_reference_start + 1,
        rdaln.template_length]))
    print "\n".join([ref+" (ref)",pair,query+" (query)"])    
	         
def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print __doc__
        sys.exit(1)
    if len(sys.argv) == 2:
        if sys.argv[-1].endswith(".bam"):
            bam = pysam.AlignmentFile(sys.argv[-1],"rb")
        elif sys.argv[-1].endswith(".sam"):
            bam = pysam.AlignmentFile(sys.argv[-1],"r")
        else:
            print __doc__
            sys.exit(1)
        for sa in bam:
            get_pairwise2(sa)
    elif len(sys.argv) in [3,4]:
        get_pairwise(*sys.argv[1:])
    elif sys.stdin:
        for line in sys.stdin:
            if line.startswith("#") or not line.strip():
                continue
            line = line.split("\t")
            qseq = line[9]
            cigar = line[5]
            mdlist = filter(lambda x:x.startswith("MD"),line[11:-1])
            if mdlist:
                md = mdlist[0].split(":")[-1]
            else:
                md = None
            print "\t".join(line[:9])            
            if cigar == "*":
                print "Unmapped read"
                continue
            get_pairwise(qseq,cigar,md)
    else:
        print __doc__
        sys.exit(1)
        
if __name__ == "__main__":
    main()

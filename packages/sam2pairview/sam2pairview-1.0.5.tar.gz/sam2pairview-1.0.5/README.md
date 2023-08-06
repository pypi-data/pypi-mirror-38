sam2pairview
============

sam2pairview takes a SAM|BAM file and uses the CIGAR and MD tag to reconstruct the pairwise alignment of each read. 


Requirements
------------

pysam


Installation
------------

pip install sam2pairview


Usage
-------

    sam2pairview bamfile|samfile

or 
    sam2pairview queryseq cigarstring [md_tag]


Output
-------

sam2pairview currently supports the following CIGAR elements for reconstructing the alignment:

* M: Alignment match. The MD tag is used to determine if this is a sequence match or mismatch.
* I: Insertion to the reference, indicated by '-' on the reference sequence.
* D: Deletion from the reference, indicated '-' on the read sequence.
* N: Skipped region from the reference, indicated by '.' on the read and 'N' on the reference sequence.
* S: Soft clipping. These characters are represented normally on the read sequence, and as 'N's on the reference sequence.
* H: Hard clipping. These characters are no longer present in the read sequence, so this value is skipped.
* P: Padding. Represented as an * in both the read and reference sequences.
* =: Sequence match. Treated the same as 'M'.
* X: Sequence mismatch. Treated the same as 'M'.

Each line of input has a corresponding four lines of output. The first line serves as the header, and reproduces the first nine mandatory fields from the SAM entry. The second line is the read itself, the third indicates sequence matches, and the fourth represents the reference sequence.

So, an input like this:

    CRATOS:145:D1UH5ACXX:2:1308:6211:53528	153	Zv9_scaffold3453	49562	26	1S15M1D65M2I18M	=	49562	0	GCCTGAGAACAAGTGAGAAAGAAACTCATTCCTGTCTTTCAATGAGTGCTTTTGTGCATTTAGGAGAACTAGGCAGCACACATTTAGGGCTGAAAGATGNA	(CCDCCCCAEECCDFFFFFFFHECHFHJIHDJIIIIJJJJJJJJJJJJIHGIFJJIGJJJIIIIIIJIJIJIGIIHGFCCJJJJJIJJHGHHHFFFDA1#C	PG:Z:novoalign	AS:i:206	UQ:i:206	NM:i:7	MD:Z:15^T35A30C7C6G1

Would produce an output like this:

    CRATOS:145:D1UH5ACXX:2:1308:6211:53528	153	Zv9_scaffold3453	49562	26	1S15M1D65M2I18M	=	49562	0
    GCCTGAGAACAAGTGA-GAAAGAAACTCATTCCTGTCTTTCAATGAGTGCTTTTGTGCATTTAGGAGAACTAGGCAGCACACATTTAGGGCTGAAAGATGNA
     ||||||||||||||| ||||||||||||||||||||||||||||||||||| |||||||||||||||||||||||||||||  | ||||||| |||||| |
    NCCTGAGAACAAGTGATGAAAGAAACTCATTCCTGTCTTTCAATGAGTGCTTATGTGCATTTAGGAGAACTAGGCAGCACAC--TCAGGGCTGCAAGATGGA

In the event that the MD tag is not detected & the CIGAR contains characters that require the MD tag to resolve, or if an unsupported character is detected in the CIGAR, the program maintains the four-line periodicity of the output by printing the header output, an error message, and two blank lines.



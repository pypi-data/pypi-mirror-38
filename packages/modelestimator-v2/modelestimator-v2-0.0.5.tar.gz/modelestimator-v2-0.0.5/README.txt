Usage: modelestimator <format> <options> infiles

<format> should be either FASTA, STOCKHOLM or PHYLIP
Output is a rate matrix and residue distribution vector.
        
Options:
    -threshold or -t <f> 
	Stop when consecutive iterations do not change by more than <f>. Default is 0.001.
    -bootstrap or -b <r>
	Perform bootstrapping on multialignment with <r> resamplings. Only one infile should be given in this mode. Returns bootstrap norm.

Example usage:
    modelestimator fasta -t 0.001 file1.fa file2.fa file3.fa
    modelestimator fasta -b 200 file.fa
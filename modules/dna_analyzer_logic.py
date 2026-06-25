import re
import pandas as pd

def validate_dna_sequence(sequence):
    """
    Validates if the provided sequence contains only valid DNA characters (A, T, C, G).
    Allows case-insensitive inputs.
    """
    if not sequence:
        return False
    cleaned = sequence.strip().upper()
    if re.search(r'[^ATCG]', cleaned):
        return False
    return True

def clean_sequence(sequence):
    """
    Cleans the sequence by removing whitespaces, newlines, and converting to uppercase.
    """
    return "".join(sequence.split()).upper()

def calculate_sequence_metrics(sequence):
    """
    Calculates fundamental biological metrics: length, nucleotide counts, and AT/GC percentages.
    """
    seq_len = len(sequence)
    if seq_len == 0:
        return {"length": 0, "gc_percentage": 0, "at_percentage": 0, "frequencies": {"A": 0, "T": 0, "C": 0, "G": 0}}
    
    counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "C": sequence.count("C"),
        "G": sequence.count("G")
    }
    
    gc_count = counts["G"] + counts["C"]
    at_count = counts["A"] + counts["T"]
    
    gc_percentage = round((gc_count / seq_len) * 100, 1)
    at_percentage = round((at_count / seq_len) * 100, 1)
    
    return {
        "length": seq_len,
        "gc_percentage": gc_percentage,
        "at_percentage": at_percentage,
        "frequencies": counts
    }

def generate_molecular_utilities(sequence):
    """
    Generates standard molecular biology downstream product utility outputs.
    Handles Reverse Complement, mRNA Transcription, and Protein Translation mapping.
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_complement = "".join([complement[base] for base in reversed(sequence)])
    
    mrna = sequence.replace('T', 'U')
    
    codon_map = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    
    protein = ""
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3]
        amino_acid = codon_map.get(codon, '?')
        protein += amino_acid
        
    return {
        "reverse_complement": reverse_complement,
        "mrna": mrna,
        "protein": protein
    }

def track_snps(user_sequence):
    """
    Compares the user sequence against a standard reference sequence 
    to track Single Nucleotide Polymorphisms (SNPs) and potential clinical impacts.
    """
    reference_sequence = "ATGCGATCGATCGATCGATCGATC"
    
    snps_found = []
    min_len = min(len(user_sequence), len(reference_sequence))
    
    variant_db = {
        3: {"rsid": "rs121913527", "condition": "Increased Risk of Cardiovascular Traits"},
        8: {"rsid": "rs1801133", "condition": "Altered Folate Metabolism Sensitivity"},
        12: {"rsid": "rs6311", "condition": "Altered Neurotransmitter Receptor Efficiency"},
        18: {"rsid": "rs7412", "condition": "Altered Lipid Metabolism/Alzheimer susceptibility"},
    }
    
    for i in range(min_len):
        ref_base = reference_sequence[i]
        user_base = user_sequence[i]
        
        if ref_base != user_base:
            position = i + 1
            
            if position in variant_db:
                snps_found.append({
                    "Position": f"Base {position}",
                    "Reference Base": ref_base,
                    "Observed Variant": user_base,
                    "dbSNP rsID": variant_db[position]["rsid"],
                    "Reported Clinical Impact / Association": variant_db[position]["condition"]
                })
            else:
                snps_found.append({
                    "Position": f"Base {position}",
                    "Reference Base": ref_base,
                    "Observed Variant": user_base,
                    "dbSNP rsID": "rs_Custom_Variant",
                    "Reported Clinical Impact / Association": "Novel Genomic Variation / Unknown Significance (VUS)"
                })
                
    return snps_found

def generate_3d_helix_coordinates(sequence):
    """
    Generates dynamic mathematical 3D double helix coordinates 
    mapped exactly to the length of the analyzed DNA sequence.
    """
    import numpy as np
    
    length = len(sequence)
    if length == 0:
        return pd.DataFrame()
        
    t = np.linspace(0, length * 0.5, length)
    
    x1 = np.cos(2 * np.pi * t)
    y1 = np.sin(2 * np.pi * t)
    z1 = np.arange(length)
    
    x2 = np.cos(2 * np.pi * t + np.pi)
    y2 = np.sin(2 * np.pi * t + np.pi)
    z2 = np.arange(length)
    
    data = []
    for i in range(length):
        base = sequence[i]
        color_map = {'A': 'Adenine (A)', 'T': 'Thymine (T)', 'C': 'Cytosine (C)', 'G': 'Guanine (G)'}
        label = color_map.get(base, 'Unknown')
        
        data.append({'X': x1[i], 'Y': y1[i], 'Z': z1[i], 'Base': label, 'Strand': 'Strand A'})
        data.append({'X': x2[i], 'Y': y2[i], 'Z': z2[i], 'Base': label, 'Strand': 'Strand B'})
        
    return pd.DataFrame(data)
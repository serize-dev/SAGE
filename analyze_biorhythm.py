#!/usr/bin/env python3
import struct
import sys
from datetime import datetime, timedelta
import math

def read_nes_header(rom_data):
    """Parse NES ROM header"""
    if rom_data[:4] != b'NES\x1a':
        raise ValueError("Not a valid NES ROM")
    
    prg_banks = rom_data[4]
    chr_banks = rom_data[5]
    flags6 = rom_data[6]
    flags7 = rom_data[7]
    
    prg_size = prg_banks * 16384  # 16KB per bank
    chr_size = chr_banks * 8192    # 8KB per bank
    
    return {
        'prg_banks': prg_banks,
        'chr_banks': chr_banks,
        'prg_size': prg_size,
        'chr_size': chr_size,
        'prg_start': 16,  # Header is 16 bytes
        'chr_start': 16 + prg_size
    }

def search_text_patterns(rom_data):
    """Search for text patterns in ROM"""
    text_patterns = []
    
    # Convert to uppercase for searching
    rom_upper = rom_data.upper()
    
    # Search for specific strings
    search_terms = [
        b'BIORHYTHM', b'PHYSICAL', b'SENSITIVITY', b'INTELLECTUAL',
        b'GOODE', b'DOB', b'KANSAS', b'GAME'
    ]
    
    for term in search_terms:
        pos = 0
        while True:
            pos = rom_upper.find(term, pos)
            if pos == -1:
                break
            text_patterns.append((pos, term.decode('ascii')))
            pos += 1
    
    return sorted(text_patterns)

def find_biorhythm_calculations(rom_data, header_info):
    """Look for potential biorhythm calculation routines"""
    prg_start = header_info['prg_start']
    prg_end = prg_start + header_info['prg_size']
    
    # Biorhythm calculations typically involve:
    # - Days since birth calculation
    # - Sine wave calculations (23, 28, 33 day cycles)
    # - Date arithmetic
    
    patterns = []
    
    # Look for the magic numbers 23, 28, 33 (biorhythm cycle lengths)
    for i in range(prg_start, prg_end - 1):
        if rom_data[i] == 23 or rom_data[i] == 28 or rom_data[i] == 33:
            patterns.append((i, f"Possible cycle length: {rom_data[i]}"))
    
    return patterns

def analyze_chr_rom(rom_data, header_info):
    """Analyze CHR-ROM for biorhythm graphics"""
    if header_info['chr_banks'] == 0:
        return []
    
    chr_start = header_info['chr_start']
    chr_end = chr_start + header_info['chr_size']
    
    # Look for tile patterns that might represent the biorhythm graph
    # This would require more sophisticated pattern matching
    
    return [(chr_start, f"CHR-ROM starts at {hex(chr_start)}, size: {header_info['chr_size']} bytes")]

def main():
    rom_file = "/home/user/Projects/Bases Loaded II - Second Season (USA).nes"
    
    with open(rom_file, 'rb') as f:
        rom_data = f.read()
    
    print("=== NES ROM Analysis: Biorhythm Feature ===\n")
    
    # Parse header
    header_info = read_nes_header(rom_data)
    print(f"PRG-ROM: {header_info['prg_banks']} banks ({header_info['prg_size']} bytes)")
    print(f"CHR-ROM: {header_info['chr_banks']} banks ({header_info['chr_size']} bytes)\n")
    
    # Search for text
    print("=== Text Pattern Search ===")
    text_patterns = search_text_patterns(rom_data)
    if text_patterns:
        for pos, text in text_patterns:
            print(f"Found '{text}' at offset {hex(pos)}")
    else:
        print("No direct text matches found")
    
    # Search for biorhythm calculations
    print("\n=== Potential Biorhythm Calculations ===")
    calc_patterns = find_biorhythm_calculations(rom_data, header_info)
    for pos, desc in calc_patterns[:20]:  # Limit output
        print(f"Offset {hex(pos)}: {desc}")
    
    # Look for specific byte patterns
    print("\n=== Searching for 'dob' string ===")
    dob_pos = rom_data.find(b'dob')
    if dob_pos != -1:
        context_start = max(0, dob_pos - 20)
        context_end = min(len(rom_data), dob_pos + 20)
        context = rom_data[context_start:context_end]
        print(f"Found 'dob' at offset {hex(dob_pos)}")
        print(f"Context: {context}")
        
        # Try to decode as ASCII
        printable = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in context])
        print(f"ASCII: {printable}")

if __name__ == "__main__":
    main()
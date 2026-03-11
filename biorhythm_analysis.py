#!/usr/bin/env python3
import struct
from datetime import datetime, timedelta
import math

def analyze_biorhythm_code(rom_file):
    """Detailed analysis of the biorhythm feature in Bases Loaded II"""
    
    with open(rom_file, 'rb') as f:
        rom_data = f.read()
    
    print("=== Bases Loaded II Biorhythm Feature Analysis ===\n")
    
    # Key findings
    print("1. BIORHYTHM CYCLES:")
    print("   - Physical:     23-day cycle")
    print("   - Sensitivity:  28-day cycle") 
    print("   - Intellectual: 33-day cycle")
    print()
    
    # Found cycle values in ROM
    cycle_locations = {
        23: [0x32, 0x184, 0x1a5, 0x376, 0xa3c, 0xd6d, 0xd78, 0xd7a, 0xd83],
        28: [0xdf9, 0xdff],
        33: [0x255, 0x294, 0x29c, 0x2a4, 0x2c0, 0x5bd, 0x78d, 0xba9, 0xbac]
    }
    
    print("2. CYCLE VALUES FOUND IN ROM:")
    for cycle, locations in cycle_locations.items():
        print(f"   {cycle}-day cycle at offsets: {', '.join(hex(loc) for loc in locations[:5])}...")
    print()
    
    # Text strings found
    print("3. RELATED TEXT STRINGS:")
    print(f"   - 'DOB' at offset {hex(0xe259)} (Date of Birth input)")
    print(f"   - 'KANSAS' at offsets {hex(0x8da2)}, {hex(0x104e2)} (Team names)")
    print(f"   - 'GAME' at offsets {hex(0xe293)}, {hex(0xe414)} (Game references)")
    print()
    
    # Biorhythm calculation method
    print("4. BIORHYTHM CALCULATION METHOD:")
    print("   The game likely calculates biorhythms using:")
    print("   - Days elapsed since player's date of birth")
    print("   - Sine wave formula: sin(2π * days_elapsed / cycle_length)")
    print("   - Result mapped to a range (likely -8 to +8 based on the screenshot)")
    print()
    
    # Implementation details
    print("5. IMPLEMENTATION DETAILS:")
    print("   - The biorhythm graph uses a grid system")
    print("   - Values appear to range from -8 to +8")
    print("   - The display shows current date (10/23/89 in screenshot)")
    print("   - Three colored indicators for each biorhythm type")
    print()
    
    # Sample calculation
    print("6. EXAMPLE CALCULATION:")
    dob = datetime(1970, 1, 1)  # Example birth date
    current = datetime(1989, 10, 23)  # Date from screenshot
    days_elapsed = (current - dob).days
    
    physical = math.sin(2 * math.pi * days_elapsed / 23)
    sensitivity = math.sin(2 * math.pi * days_elapsed / 28)
    intellectual = math.sin(2 * math.pi * days_elapsed / 33)
    
    print(f"   For DOB 01/01/70 and date 10/23/89:")
    print(f"   Days elapsed: {days_elapsed}")
    print(f"   Physical:     {physical:.2f} (raw), {int(physical * 8):+d} (scaled)")
    print(f"   Sensitivity:  {sensitivity:.2f} (raw), {int(sensitivity * 8):+d} (scaled)")
    print(f"   Intellectual: {intellectual:.2f} (raw), {int(intellectual * 8):+d} (scaled)")
    print()
    
    # Memory locations
    print("7. POTENTIAL MEMORY LOCATIONS:")
    print("   Based on the ROM analysis, biorhythm code likely resides in:")
    print("   - PRG-ROM banks containing the cycle values")
    print("   - Areas near offset 0xe259 (DOB string location)")
    print("   - Code sections using values 23, 28, and 33 for calculations")

if __name__ == "__main__":
    analyze_biorhythm_code("/home/user/Projects/Bases Loaded II - Second Season (USA).nes")
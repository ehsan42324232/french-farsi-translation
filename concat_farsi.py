#!/usr/bin/env python3
"""
Script to concatenate all Farsi translation files in numerical order.
Each file content starts on a new line in the output.
"""

import os
import re
import sys
from pathlib import Path

def get_file_number(filename):
    """Extract the number from filename like '23_farsi.txt' -> 23"""
    match = re.match(r'(\d+)_farsi\.txt', filename)
    return int(match.group(1)) if match else float('inf')

def concat_farsi_files(input_dir='.', output_file='complete_farsi_translation.txt'):
    """
    Concatenate all *_farsi.txt files in numerical order.
    
    Args:
        input_dir: Directory containing the farsi files (default: current directory)
        output_file: Output filename for concatenated content
    """
    
    # Find all farsi translation files
    farsi_files = []
    for filename in os.listdir(input_dir):
        if filename.endswith('_farsi.txt') and re.match(r'\d+_farsi\.txt', filename):
            farsi_files.append(filename)
    
    if not farsi_files:
        print("No Farsi translation files found!")
        return False
    
    # Sort files by number
    farsi_files.sort(key=get_file_number)
    
    print(f"Found {len(farsi_files)} Farsi translation files")
    print("Files to be concatenated:")
    for filename in farsi_files:
        file_num = get_file_number(filename)
        file_path = os.path.join(input_dir, filename)
        file_size = os.path.getsize(file_path)
        print(f"  {file_num:2d}: {filename} ({file_size:,} bytes)")
    
    # Concatenate files
    total_chars = 0
    total_lines = 0
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filename in enumerate(farsi_files):
                file_path = os.path.join(input_dir, filename)
                file_num = get_file_number(filename)
                
                print(f"Processing file {i+1}/{len(farsi_files)}: {filename}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read().strip()
                        
                        if content:
                            # Add file header comment (optional)
                            outfile.write(f"# --- File {file_num}: {filename} ---\n")
                            
                            # Write content with newline
                            outfile.write(content)
                            outfile.write('\n\n')  # Double newline between files
                            
                            # Statistics
                            total_chars += len(content)
                            total_lines += content.count('\n')
                        
                except UnicodeDecodeError:
                    print(f"Warning: Could not read {filename} with UTF-8 encoding")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        print(f"\n✅ Successfully created: {output_file}")
        print(f"📊 Statistics:")
        print(f"   • Files processed: {len(farsi_files)}")
        print(f"   • Total characters: {total_chars:,}")
        print(f"   • Total lines: {total_lines:,}")
        print(f"   • Output file size: {os.path.getsize(output_file):,} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error creating output file: {e}")
        return False

def main():
    """Main function with command line argument support"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Concatenate Farsi translation files in numerical order',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 concat_farsi.py                          # Use current directory
  python3 concat_farsi.py -d /path/to/files       # Specify input directory
  python3 concat_farsi.py -o my_translation.txt   # Custom output filename
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='Directory containing Farsi files (default: current directory)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='complete_farsi_translation.txt',
        help='Output filename (default: complete_farsi_translation.txt)'
    )
    
    parser.add_argument(
        '--no-headers',
        action='store_true',
        help='Do not include file header comments in output'
    )
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist!")
        sys.exit(1)
    
    print(f"🔍 Looking for Farsi files in: {os.path.abspath(args.directory)}")
    print(f"📝 Output file: {args.output}")
    print("-" * 50)
    
    success = concat_farsi_files(args.directory, args.output)
    
    if success:
        print(f"\n🎉 Translation concatenation completed successfully!")
        print(f"📁 Output saved as: {os.path.abspath(args.output)}")
    else:
        print("\n❌ Failed to concatenate files")
        sys.exit(1)

if __name__ == '__main__':
    main()

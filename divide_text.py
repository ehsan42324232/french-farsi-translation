#!/usr/bin/env python3
"""
Script to divide 1-4.txt into parts of approximately 1000 words each
and save them as numbered files (1.txt, 2.txt, etc.)
"""

import re
import os
from github import Github
import sys

def read_file(filename):
    """Read the content of the file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return None
    except UnicodeDecodeError:
        # Try different encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        print(f"Could not decode file {filename} with any known encoding")
        return None

def split_into_words(text):
    """Split text into words"""
    # Remove extra whitespace and split by whitespace
    words = re.findall(r'\S+', text)
    return words

def create_parts(words, words_per_part=1000):
    """Divide words into parts of approximately words_per_part words each"""
    parts = []
    current_part = []
    
    for word in words:
        current_part.append(word)
        if len(current_part) >= words_per_part:
            parts.append(' '.join(current_part))
            current_part = []
    
    # Add remaining words as the last part
    if current_part:
        parts.append(' '.join(current_part))
    
    return parts

def save_parts_locally(parts, prefix="part"):
    """Save parts as local files"""
    filenames = []
    for i, part in enumerate(parts, 1):
        filename = f"{i}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(part)
        filenames.append(filename)
        print(f"Created {filename} with {len(part.split())} words")
    return filenames

def push_to_github(filenames, repo_owner, repo_name, github_token=None):
    """Push the created files to GitHub repository"""
    if not github_token:
        print("No GitHub token provided. Files saved locally only.")
        print("To push to GitHub, provide your GitHub token as an environment variable: GITHUB_TOKEN")
        return
    
    try:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            try:
                # Try to get existing file
                existing_file = repo.get_contents(filename)
                # Update existing file
                repo.update_file(
                    filename,
                    f"Update {filename} - part of divided text",
                    content,
                    existing_file.sha
                )
                print(f"Updated {filename} in GitHub repository")
            except:
                # Create new file
                repo.create_file(
                    filename,
                    f"Add {filename} - part of divided text",
                    content
                )
                print(f"Created {filename} in GitHub repository")
                
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")
        print("Files are saved locally. You can manually upload them to GitHub.")

def main():
    """Main function"""
    input_file = "1-4.txt"
    
    print(f"Reading {input_file}...")
    content = read_file(input_file)
    
    if content is None:
        return
    
    print(f"File size: {len(content)} characters")
    
    # Split into words
    words = split_into_words(content)
    print(f"Total words: {len(words)}")
    
    # Create parts
    parts = create_parts(words, words_per_part=1000)
    print(f"Created {len(parts)} parts")
    
    # Save parts locally
    filenames = save_parts_locally(parts)
    
    # Try to push to GitHub (requires GITHUB_TOKEN environment variable)
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        push_to_github(filenames, "ehsan42324232", "french-farsi-translation", github_token)
    else:
        print("\nTo automatically push to GitHub, set your GitHub token:")
        print("export GITHUB_TOKEN='your_github_token_here'")
        print("Then run the script again, or manually upload the created files.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to push divided text files (1.txt, 2.txt, etc.) to GitHub repository
Run this script in the directory where your numbered .txt files are located
"""

import os
import glob
import time
from github import Github

def find_numbered_files():
    """Find all numbered .txt files in current directory"""
    files = []
    
    # Look for files like 1.txt, 2.txt, etc.
    for filename in glob.glob("*.txt"):
        try:
            # Check if filename is just a number with .txt extension
            name_part = filename.replace('.txt', '')
            if name_part.isdigit():
                files.append((int(name_part), filename))
        except:
            continue
    
    # Sort by number
    files.sort(key=lambda x: x[0])
    return [f[1] for f in files]

def push_files_to_github(filenames, owner, repo, github_token, branch='main'):
    """Push files to GitHub repository"""
    
    if not github_token:
        print("❌ GitHub token is required!")
        print("Set your token with: export GITHUB_TOKEN='your_token_here'")
        return False
    
    try:
        g = Github(github_token)
        repository = g.get_repo(f"{owner}/{repo}")
        
        print(f"📁 Found {len(filenames)} files to upload")
        print(f"🎯 Target repository: {owner}/{repo}")
        print(f"🌿 Branch: {branch}")
        print()
        
        successful_uploads = 0
        failed_uploads = 0
        
        for i, filename in enumerate(filenames, 1):
            try:
                print(f"📤 [{i}/{len(filenames)}] Processing {filename}...", end=' ')
                
                # Read file content
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                word_count = len(content.split())
                
                # Check if file already exists in repository
                try:
                    existing_file = repository.get_contents(filename, ref=branch)
                    # Update existing file
                    repository.update_file(
                        filename,
                        f"Update {filename} - part {i} ({word_count} words)",
                        content,
                        existing_file.sha,
                        branch=branch
                    )
                    print(f"✅ Updated ({word_count} words)")
                except:
                    # Create new file
                    repository.create_file(
                        filename,
                        f"Add {filename} - part {i} ({word_count} words)",
                        content,
                        branch=branch
                    )
                    print(f"✅ Created ({word_count} words)")
                
                successful_uploads += 1
                
                # Rate limiting: small delay between uploads
                if i % 10 == 0:  # Longer pause every 10 files
                    print("⏸️  Pausing to avoid rate limits...")
                    time.sleep(2)
                else:
                    time.sleep(0.3)
                
            except FileNotFoundError:
                print(f"❌ File not found")
                failed_uploads += 1
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}...")
                failed_uploads += 1
        
        print()
        print("=" * 50)
        print(f"📊 Upload Summary:")
        print(f"   ✅ Successful: {successful_uploads}")
        print(f"   ❌ Failed: {failed_uploads}")
        print(f"   📁 Total files: {len(filenames)}")
        
        if successful_uploads > 0:
            print(f"🎉 Files uploaded to: https://github.com/{owner}/{repo}")
        
        return failed_uploads == 0
        
    except Exception as e:
        print(f"❌ Error accessing GitHub repository: {e}")
        return False

def main():
    """Main function"""
    
    print("🔍 Searching for numbered text files...")
    
    # Find all numbered .txt files
    files = find_numbered_files()
    
    if not files:
        print("❌ No numbered .txt files found in current directory!")
        print("   Expected files like: 1.txt, 2.txt, 3.txt, etc.")
        return
    
    print(f"📋 Found files: {files[:5]}")
    if len(files) > 5:
        print(f"   ... and {len(files) - 5} more files")
    print()
    
    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠️  GitHub token not found!")
        print("   1. Create a token at: https://github.com/settings/tokens")
        print("   2. Give it 'repo' permissions")
        print("   3. Set it with: export GITHUB_TOKEN='your_token_here'")
        print("   4. Run this script again")
        return
    
    # Configuration
    owner = "ehsan42324232"
    repo = "french-farsi-translation"
    
    # Confirm upload
    response = input(f"📤 Upload {len(files)} files to {owner}/{repo}? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Upload cancelled")
        return
    
    # Upload files
    success = push_files_to_github(files, owner, repo, github_token)
    
    if success:
        print("🎉 All files uploaded successfully!")
    else:
        print("⚠️  Some files failed to upload. Check the output above.")

if __name__ == "__main__":
    main()

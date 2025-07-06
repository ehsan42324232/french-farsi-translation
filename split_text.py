import re
import os

def split_text_file(input_file, words_per_chunk=1000):
    """
    Split a text file into chunks of approximately 1000 words each,
    ensuring sentences are complete.
    """
    
    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(input_file, 'r', encoding='latin-1') as f:
            text = f.read()
    
    # Split text into words
    words = text.split()
    total_words = len(words)
    
    print(f"Total words in file: {total_words}")
    print(f"Target words per chunk: {words_per_chunk}")
    
    # Create output directory if it doesn't exist
    output_dir = "split_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chunk_number = 1
    current_position = 0
    
    while current_position < total_words:
        # Get approximately 1000 words
        end_position = min(current_position + words_per_chunk, total_words)
        chunk_words = words[current_position:end_position]
        chunk_text = ' '.join(chunk_words)
        
        # If we're not at the end of the file, extend to complete the sentence
        if end_position < total_words:
            # Look for sentence endings after our target word count
            remaining_text = ' '.join(words[end_position:])
            
            # Find the next sentence ending (., !, ?, or paragraph break)
            sentence_end_pattern = r'^.*?[.!?]\s+'
            match = re.match(sentence_end_pattern, remaining_text, re.DOTALL)
            
            if match:
                # Add the rest of the sentence
                sentence_completion = match.group(0).rstrip()
                chunk_text += ' ' + sentence_completion
                # Update end_position to account for the added words
                added_words = len(sentence_completion.split())
                end_position += added_words
            else:
                # If no sentence ending found nearby, look for paragraph break
                paragraph_pattern = r'^.*?\n\s*\n'
                match = re.match(paragraph_pattern, remaining_text, re.DOTALL)
                if match:
                    paragraph_completion = match.group(0).rstrip()
                    chunk_text += ' ' + paragraph_completion
                    added_words = len(paragraph_completion.split())
                    end_position += added_words
        
        # Write the chunk to a file
        output_filename = os.path.join(output_dir, f"{chunk_number}.txt")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(chunk_text.strip())
        
        actual_word_count = len(chunk_text.split())
        print(f"Created {output_filename} with {actual_word_count} words")
        
        # Move to the next chunk
        current_position = end_position
        chunk_number += 1
    
    print(f"\nSplitting complete! Created {chunk_number - 1} files in '{output_dir}' directory.")
    return chunk_number - 1

if __name__ == "__main__":
    # Split the complete.txt file
    input_file = "complete.txt"
    
    if os.path.exists(input_file):
        num_files = split_text_file(input_file, 1000)
        print(f"\nSuccessfully split {input_file} into {num_files} files.")
    else:
        print(f"Error: {input_file} not found in current directory.")
        print("Make sure you're running this script in the same directory as complete.txt")

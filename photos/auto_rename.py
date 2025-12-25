import os
import time
import pathlib
import sys

def main():
    # Set the folder to the directory containing this script
    folder = pathlib.Path(__file__).parent
    print(f"Monitoring {folder}...")
    print("Press Ctrl+C to stop.")

    while True:
        try:
            # 1. Get all files
            # Filter out .DS_Store and this script itself
            all_files = [
                f for f in folder.iterdir() 
                if f.is_file() and f.name != ".DS_Store" and f.name != pathlib.Path(__file__).name
            ]
            
            # 2. Separate into numbered files (N.jpg) and regular image files to be renamed
            numbered_files = []
            other_files = []
            
            for f in all_files:
                stem = f.stem
                suffix = f.suffix.lower()
                
                # Check if it is a number and has .jpg extension
                if stem.isdigit() and suffix == ".jpg":
                    numbered_files.append(int(stem))
                # Identify other images (jpg, png, jpeg, etc.)
                elif suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']: 
                    other_files.append(f)

            # Sort the numbered files to detect gaps
            numbered_files.sort()
            
            # 3. Gap Filling / Re-sorting
            # We want files to be 1.jpg, 2.jpg... N.jpg
            # If we detect a gap (e.g. 1, 3 exists but 2 is missing), we rename 3->2 using the logic that
            # we fill slots sequentially.
            
            current_max = 0
            
            # Use a set for fast lookup of existing destinations during this cycle (optional, but good for safety)
            # Actually, since we iterate in order, we just need to know the next target index.
            
            for i, num in enumerate(numbered_files):
                expected = i + 1
                if num != expected:
                    # Gap detected or shift needed
                    src = folder / f"{num}.jpg"
                    dst = folder / f"{expected}.jpg"
                    
                    if not dst.exists():
                        print(f"[Re-sort] Renaming {src.name} -> {dst.name}")
                        try:
                            src.rename(dst)
                            current_max = expected
                        except OSError as e:
                            print(f"Error renaming {src.name}: {e}")
                            # Keep current_max as is or handle error? 
                            # If rename fails, we might have a hole. 
                            # Determine max based on 'num' (which is still there) or 'expected'?
                            # Let's assume on error we don't increment max cleanly, 
                            # but next loop will retry.
                            pass
                    else:
                        # This should theoretically not happen if we sort and fill from 1
                        print(f"Warning: Destination {dst.name} already exists. Skipping {src.name}.")
                        # If we skip, the current file 'num' is still at 'num'.
                        current_max = max(current_max, num)
                else:
                    current_max = expected

            # 4. New File Handling
            # current_max is now the count of correctly sequenced files (or the last used number)
            # We append new files after current_max.
            
            if other_files:
                # Sort by name to have deterministic order
                other_files.sort(key=lambda x: x.name)
                
                for f in other_files:
                    current_max += 1
                    dst = folder / f"{current_max}.jpg"
                    
                    # Ensure we don't overwrite (though current_max should be free)
                    while dst.exists():
                        current_max += 1
                        dst = folder / f"{current_max}.jpg"
                        
                    print(f"[New] Renaming {f.name} -> {dst.name}")
                    try:
                        f.rename(dst)
                    except OSError as e:
                        print(f"Error renaming {f.name}: {e}")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nStopping...")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()

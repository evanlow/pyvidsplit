#!/usr/bin/env python3
"""
Video Concatenation Script

Concatenates (stitches) two MP4 video files into a single output file.

Usage:
    python concat_video.py input1.mp4 input2.mp4
    python concat_video.py input1.mp4 input2.mp4 -o output.mp4
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple, Optional


def validate_input_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate that input file exists and is readable.
    
    Args:
        file_path: Path to input file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if file_path is None or file_path.strip() == "":
        return False, "Input file path is empty"
    
    path = Path(file_path)
    
    if not path.exists():
        return False, f"Input file does not exist: {file_path}"
    
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"
    
    if not os.access(file_path, os.R_OK):
        return False, f"Input file is not readable: {file_path}"
    
    # Check file extension (case-insensitive)
    if path.suffix.lower() not in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
        return False, f"File does not appear to be a video file: {file_path}"
    
    return True, ""


def generate_output_filename(input1_path: str, input2_path: str) -> str:
    """
    Generate output filename for concatenated video.
    
    Args:
        input1_path: Path to first input file
        input2_path: Path to second input file
        
    Returns:
        Generated output filename
    """
    path1 = Path(input1_path)
    path2 = Path(input2_path)
    
    # Use first file's directory and extension
    parent = path1.parent
    suffix = path1.suffix
    
    # Create descriptive name
    stem1 = path1.stem
    stem2 = path2.stem
    
    output = parent / f"{stem1}_concat_{stem2}{suffix}"
    
    return str(output)


def concat_videos(input_file1: str, input_file2: str, output_file: str) -> Tuple[bool, str]:
    """
    Concatenate two video files into a single output file.
    
    Args:
        input_file1: Path to first input video file
        input_file2: Path to second input video file
        output_file: Path for output file
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        from moviepy import VideoFileClip, concatenate_videoclips
    except ImportError:
        return False, "moviepy is not installed. Install with: pip install moviepy"
    
    try:
        # Load first video clip
        print(f"Loading video 1: {input_file1}")
        video1 = VideoFileClip(input_file1)
        
        # Defensive: Check if duration is valid
        duration1 = video1.duration
        if duration1 is None or duration1 <= 0:
            video1.close()
            return False, f"Unable to determine duration for video 1: {input_file1}"
        
        print(f"Video 1 duration: {duration1:.2f} seconds")
        
        # Load second video clip
        print(f"Loading video 2: {input_file2}")
        video2 = VideoFileClip(input_file2)
        
        # Defensive: Check if duration is valid
        duration2 = video2.duration
        if duration2 is None or duration2 <= 0:
            video1.close()
            video2.close()
            return False, f"Unable to determine duration for video 2: {input_file2}"
        
        print(f"Video 2 duration: {duration2:.2f} seconds")
        
        # Concatenate videos
        print(f"Concatenating videos...")
        final_video = concatenate_videoclips([video1, video2])
        
        total_duration = final_video.duration or 0
        print(f"Output video duration: {total_duration:.2f} seconds")
        
        # Write output file
        print(f"Writing output: {output_file}")
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # Clean up
        final_video.close()
        video1.close()
        video2.close()
        
        return True, ""
        
    except Exception as e:
        return False, f"Error concatenating videos: {str(e)}"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Concatenate two MP4 video files into a single output file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s video1.mp4 video2.mp4
  %(prog)s first.mp4 second.mp4 -o combined.mp4
  %(prog)s intro.mp4 main.mp4 --output final_video.mp4
        """
    )
    
    parser.add_argument('input1', help='First input video file')
    parser.add_argument('input2', help='Second input video file')
    parser.add_argument('-o', '--output', default=None,
                        help='Output filename (default: input1_concat_input2.mp4)')
    
    args = parser.parse_args()
    
    # Validate first input file
    is_valid, error_msg = validate_input_file(args.input1)
    if not is_valid:
        print(f"Error with first input: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Validate second input file
    is_valid, error_msg = validate_input_file(args.input2)
    if not is_valid:
        print(f"Error with second input: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output:
        output_file = args.output
    else:
        output_file = generate_output_filename(args.input1, args.input2)
    
    # Check if output file already exists
    if os.path.exists(output_file):
        print(f"Warning: Output file already exists and will be overwritten: {output_file}")
    
    # Concatenate the videos
    success, error_msg = concat_videos(args.input1, args.input2, output_file)
    
    if success:
        print(f"\n✓ Successfully concatenated videos into:")
        print(f"  Output: {output_file}")
        sys.exit(0)
    else:
        print(f"\nError: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

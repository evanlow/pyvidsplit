#!/usr/bin/env python3
"""
Audio Removal Script

Removes audio from video files, creating a silent video.

Usage:
    python remove_audio.py input.mp4
    python remove_audio.py input.mov -o silent_output.mp4
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple


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
    if path.suffix.lower() not in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']:
        return False, f"File does not appear to be a video file: {file_path}"
    
    return True, ""


def generate_output_filename(input_path: str) -> str:
    """
    Generate output filename for silent video.
    
    Args:
        input_path: Path to input file
        
    Returns:
        Generated output filename
    """
    path = Path(input_path)
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    output = parent / f"{stem}_silent{suffix}"
    
    return str(output)


def remove_audio(input_file: str, output_file: str, quality: str = 'medium') -> Tuple[bool, str]:
    """
    Remove audio from video file, creating a silent video.
    
    Args:
        input_file: Path to input video file
        output_file: Path for output file (without audio)
        quality: Quality preset ('high', 'medium', 'low')
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        from moviepy import VideoFileClip
    except ImportError:
        return False, "moviepy is not installed. Install with: pip install moviepy"
    
    # Defensive: Validate quality preset
    quality_map = {'high': 18, 'medium': 23, 'low': 28}
    if quality not in quality_map:
        return False, f"Invalid quality preset: {quality}. Use 'high', 'medium', or 'low'"
    
    crf = quality_map[quality]
    
    try:
        # Load video clip
        print(f"Loading video: {input_file}")
        video = VideoFileClip(input_file)
        
        # Defensive: Check if duration is valid
        duration = video.duration
        if duration is None or duration <= 0:
            video.close()
            return False, f"Unable to determine video duration: {input_file}"
        
        print(f"Video duration: {duration:.2f} seconds")
        
        # Check if video has audio
        has_audio = video.audio is not None
        if has_audio:
            print("Removing audio track...")
        else:
            print("Warning: Video has no audio track (already silent)")
        
        # Remove audio by setting audio attribute to None
        video_without_audio = video.with_audio(None)
        
        # Write output file without audio
        print(f"Writing silent video: {output_file}")
        video_without_audio.write_videofile(
            output_file,
            codec='libx264',
            audio=False,  # Explicitly disable audio
            ffmpeg_params=['-crf', str(crf)]
        )
        
        # Clean up
        video_without_audio.close()
        video.close()
        
        return True, ""
        
    except Exception as e:
        return False, f"Error removing audio from video: {str(e)}"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Remove audio from video files, creating a silent video.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp4
  %(prog)s video.mov -o silent.mp4
  %(prog)s clip.avi --output no_sound.avi
        """
    )
    
    parser.add_argument('input', help='Input video file')
    parser.add_argument('-o', '--output', default=None,
                        help='Output filename (default: input_silent.ext)')
    parser.add_argument('-q', '--quality', choices=['high', 'medium', 'low'],
                        default='medium',
                        help='Output quality preset: high (CRF 18), medium (CRF 23, default), low (CRF 28)')
    
    args = parser.parse_args()
    
    # Validate input file
    is_valid, error_msg = validate_input_file(args.input)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output:
        output_file = args.output
        # Verify output filename has valid extension
        output_ext = Path(output_file).suffix.lower()
        if output_ext and output_ext not in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']:
            print(f"Error: Unsupported output file extension: {output_ext}", file=sys.stderr)
            sys.exit(1)
    else:
        output_file = generate_output_filename(args.input)
    
    # Check if output file already exists
    if os.path.exists(output_file):
        print(f"Warning: Output file already exists and will be overwritten: {output_file}")
    
    # Check if input and output are the same (defensive programming)
    input_abs = os.path.abspath(args.input)
    output_abs = os.path.abspath(output_file)
    if input_abs == output_abs:
        print(f"Error: Input and output files are the same: {output_file}", file=sys.stderr)
        sys.exit(1)
    
    # Remove audio from video
    success, error_msg = remove_audio(args.input, output_file, args.quality)
    
    if success:
        print(f"\n✓ Successfully removed audio from video:")
        print(f"  Output: {output_file}")
        sys.exit(0)
    else:
        print(f"\nError: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

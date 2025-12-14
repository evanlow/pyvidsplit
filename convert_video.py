#!/usr/bin/env python3
"""
Video Converter Script

Converts video files from one format to another (e.g., MOV to MP4).

Usage:
    python convert_video.py input.mov
    python convert_video.py input.avi -o output.mp4
    python convert_video.py input.mkv --format mp4
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
    if path.suffix.lower() not in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']:
        return False, f"File does not appear to be a video file: {file_path}"
    
    return True, ""


def validate_output_format(format_str: str) -> Tuple[bool, str]:
    """
    Validate output format string.
    
    Args:
        format_str: Output format (e.g., 'mp4', 'avi', 'mov')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if format_str is None or format_str.strip() == "":
        return False, "Output format is empty"
    
    format_str = format_str.strip().lower()
    
    # Remove leading dot if present
    if format_str.startswith('.'):
        format_str = format_str[1:]
    
    valid_formats = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'm4v']
    
    if format_str not in valid_formats:
        return False, f"Unsupported output format: {format_str}. Supported: {', '.join(valid_formats)}"
    
    return True, ""


def generate_output_filename(input_path: str, output_format: str) -> str:
    """
    Generate output filename with new format.
    
    Args:
        input_path: Path to input file
        output_format: Desired output format (e.g., 'mp4')
        
    Returns:
        Generated output filename
    """
    path = Path(input_path)
    stem = path.stem
    parent = path.parent
    
    # Ensure format doesn't have leading dot
    if output_format.startswith('.'):
        output_format = output_format[1:]
    
    output = parent / f"{stem}.{output_format.lower()}"
    
    return str(output)


def convert_video(input_file: str, output_file: str) -> Tuple[bool, str]:
    """
    Convert video file to different format.
    
    Args:
        input_file: Path to input video file
        output_file: Path for output file
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        from moviepy import VideoFileClip
    except ImportError:
        return False, "moviepy is not installed. Install with: pip install moviepy"
    
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
        
        # Determine output format from file extension
        output_path = Path(output_file)
        output_ext = output_path.suffix.lower()
        
        # Write output file with appropriate codec
        print(f"Converting to: {output_file}")
        
        # Use appropriate codec based on output format
        if output_ext == '.mp4':
            video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        elif output_ext == '.avi':
            video.write_videofile(output_file, codec='png')
        elif output_ext == '.mov':
            video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        elif output_ext == '.webm':
            video.write_videofile(output_file, codec='libvpx', audio_codec='libvorbis')
        else:
            # Default to libx264 for other formats
            video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # Clean up
        video.close()
        
        return True, ""
        
    except Exception as e:
        return False, f"Error converting video: {str(e)}"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert video files from one format to another.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mov
  %(prog)s input.avi -o output.mp4
  %(prog)s video.mkv --format mp4
  %(prog)s source.flv -o converted.mov
        """
    )
    
    parser.add_argument('input', help='Input video file')
    parser.add_argument('-o', '--output', default=None,
                        help='Output filename (default: input filename with new extension)')
    parser.add_argument('-f', '--format', default='mp4',
                        help='Output format (default: mp4)')
    
    args = parser.parse_args()
    
    # Validate input file
    is_valid, error_msg = validate_input_file(args.input)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Validate output format
    output_format = args.format
    is_valid, error_msg = validate_output_format(output_format)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output:
        output_file = args.output
        # Verify output filename has valid extension
        output_ext = Path(output_file).suffix.lower()
        if output_ext:
            # Remove dot for validation
            ext_without_dot = output_ext[1:] if output_ext.startswith('.') else output_ext
            is_valid, error_msg = validate_output_format(ext_without_dot)
            if not is_valid:
                print(f"Error in output filename: {error_msg}", file=sys.stderr)
                sys.exit(1)
    else:
        output_file = generate_output_filename(args.input, output_format)
    
    # Check if output file already exists
    if os.path.exists(output_file):
        print(f"Warning: Output file already exists and will be overwritten: {output_file}")
    
    # Check if input and output are the same
    input_abs = os.path.abspath(args.input)
    output_abs = os.path.abspath(output_file)
    if input_abs == output_abs:
        print(f"Error: Input and output files are the same: {output_file}", file=sys.stderr)
        sys.exit(1)
    
    # Convert the video
    success, error_msg = convert_video(args.input, output_file)
    
    if success:
        print(f"\n✓ Successfully converted video:")
        print(f"  Output: {output_file}")
        sys.exit(0)
    else:
        print(f"\nError: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

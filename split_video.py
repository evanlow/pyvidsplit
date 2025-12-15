#!/usr/bin/env python3
"""
Video Splitter Script

Splits an MP4 video file into two parts at a specified duration.

Usage:
    python split_video.py input.mp4 --duration 00:05:30
    python split_video.py input.mp4 -d 300  (seconds)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple, Optional


def parse_duration(duration_str: str) -> Optional[float]:
    """
    Parse duration string to seconds.
    
    Supports formats:
    - Seconds: "300" or "300.5"
    - MM:SS: "05:30"
    - HH:MM:SS: "01:05:30"
    
    Args:
        duration_str: Duration as string
        
    Returns:
        Duration in seconds, or None if invalid
    """
    if duration_str is None:
        return None
    
    duration_str = duration_str.strip()
    
    # Try parsing as float (seconds)
    try:
        seconds = float(duration_str)
        if seconds > 0:
            return seconds
    except ValueError:
        pass
    
    # Try parsing as time format (HH:MM:SS or MM:SS)
    parts = duration_str.split(':')
    if len(parts) == 2:  # MM:SS
        try:
            minutes, seconds = int(parts[0]), float(parts[1])
            if minutes >= 0 and 0 <= seconds < 60:
                return minutes * 60 + seconds
        except ValueError:
            pass
    elif len(parts) == 3:  # HH:MM:SS
        try:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), float(parts[2])
            if hours >= 0 and 0 <= minutes < 60 and 0 <= seconds < 60:
                return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            pass
    
    return None


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


def generate_output_filenames(input_path: str) -> Tuple[str, str]:
    """
    Generate output filenames for the two parts.
    
    Args:
        input_path: Path to input file
        
    Returns:
        Tuple of (part1_path, part2_path)
    """
    path = Path(input_path)
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    part1 = parent / f"{stem}_part1{suffix}"
    part2 = parent / f"{stem}_part2{suffix}"
    
    return str(part1), str(part2)


def split_video(input_file: str, duration_seconds: float, output_part1: str, output_part2: str, quality: str = 'medium') -> Tuple[bool, str]:
    """
    Split video file into two parts at specified duration.
    
    Args:
        input_file: Path to input video file
        duration_seconds: Duration in seconds where to split
        output_part1: Path for first output file
        output_part2: Path for second output file
        quality: Quality preset ('high', 'medium', 'low')
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        from moviepy import VideoFileClip
    except ImportError:
        return False, "moviepy is not installed. Install with: pip install moviepy"
    
    # Defensive: Validate duration is positive
    if duration_seconds <= 0:
        return False, f"Duration must be positive, got: {duration_seconds}"
    
    # Defensive: Validate quality preset
    quality_map = {'high': 18, 'medium': 23, 'low': 28}
    if quality not in quality_map:
        return False, f"Invalid quality preset: {quality}. Use 'high', 'medium', or 'low'"
    
    crf = quality_map[quality]
    
    try:
        # Load video clip
        print(f"Loading video: {input_file}")
        video = VideoFileClip(input_file)
        
        # Defensive: Check if duration is valid for this video
        total_duration = video.duration
        if total_duration is None:
            video.close()
            return False, "Unable to determine video duration"
        
        if duration_seconds >= total_duration:
            video.close()
            return False, f"Split duration ({duration_seconds}s) exceeds video length ({total_duration:.2f}s)"
        
        print(f"Video duration: {total_duration:.2f} seconds")
        print(f"Splitting at: {duration_seconds:.2f} seconds")
        
        # Create first part (0 to duration)
        print(f"Creating part 1: {output_part1}")
        part1 = video.subclipped(0, duration_seconds)
        part1.write_videofile(output_part1, codec='libx264', audio_codec='aac',
                            ffmpeg_params=['-crf', str(crf)])
        part1.close()
        
        # Clean up first video object
        video.close()
        
        # Reload video for second part (avoids FFmpeg process issues)
        print(f"Creating part 2: {output_part2}")
        video2 = VideoFileClip(input_file)
        part2 = video2.subclipped(duration_seconds, video2.duration)
        part2.write_videofile(output_part2, codec='libx264', audio_codec='aac',
                            ffmpeg_params=['-crf', str(crf)])
        part2.close()
        video2.close()
        
        return True, ""
        
    except Exception as e:
        return False, f"Error splitting video: {str(e)}"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Split an MP4 video file into two parts at a specified duration.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp4 -d 300
  %(prog)s input.mp4 --duration 00:05:30
  %(prog)s input.mp4 -d 01:30:00 -o1 first.mp4 -o2 second.mp4
        """
    )
    
    parser.add_argument('input', help='Input MP4 video file')
    parser.add_argument('-d', '--duration', required=True,
                        help='Duration where to split (seconds, MM:SS, or HH:MM:SS)')
    parser.add_argument('-o1', '--output1', default=None,
                        help='Output filename for part 1 (default: input_part1.mp4)')
    parser.add_argument('-o2', '--output2', default=None,
                        help='Output filename for part 2 (default: input_part2.mp4)')
    parser.add_argument('-q', '--quality', choices=['high', 'medium', 'low'],
                        default='medium',
                        help='Output quality preset: high (CRF 18), medium (CRF 23, default), low (CRF 28)')
    
    args = parser.parse_args()
    
    # Validate input file
    is_valid, error_msg = validate_input_file(args.input)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Parse duration
    duration = parse_duration(args.duration)
    if duration is None:
        print(f"Error: Invalid duration format: {args.duration}", file=sys.stderr)
        print("Use seconds (300), MM:SS (05:30), or HH:MM:SS (01:05:30)", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filenames
    if args.output1 and args.output2:
        output_part1 = args.output1
        output_part2 = args.output2
    else:
        output_part1, output_part2 = generate_output_filenames(args.input)
    
    # Check if output files already exist
    if os.path.exists(output_part1):
        print(f"Warning: Output file already exists and will be overwritten: {output_part1}")
    if os.path.exists(output_part2):
        print(f"Warning: Output file already exists and will be overwritten: {output_part2}")
    
    # Split the video
    success, error_msg = split_video(args.input, duration, output_part1, output_part2, args.quality)
    
    if success:
        print(f"\n✓ Successfully split video into:")
        print(f"  Part 1: {output_part1}")
        print(f"  Part 2: {output_part2}")
        sys.exit(0)
    else:
        print(f"\nError: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

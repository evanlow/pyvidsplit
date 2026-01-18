#!/usr/bin/env python3
"""
Audio Splitter Script

Splits an audio file into two parts at a specified duration.
Supports M4A, MP3, WAV, AAC, FLAC, and OGG formats.

Usage:
    python split_audio.py input.m4a --duration 00:05:30
    python split_audio.py input.mp3 -d 300  (seconds)
    python split_audio.py input.wav -d 01:30:00 --quality high
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
    
    # Check file extension (case-insensitive) - audio formats
    if path.suffix.lower() not in ['.m4a', '.mp3', '.wav', '.aac', '.flac', '.ogg']:
        return False, f"File does not appear to be an audio file: {file_path}"
    
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


def split_audio(input_file: str, duration_seconds: float, output_part1: str, output_part2: str, quality: str = 'medium') -> Tuple[bool, str]:
    """
    Split audio file into two parts at specified duration.
    
    Args:
        input_file: Path to input audio file
        duration_seconds: Duration in seconds where to split
        output_part1: Path for first output file
        output_part2: Path for second output file
        quality: Quality preset ('high', 'medium', 'low')
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        from moviepy import AudioFileClip
    except ImportError:
        return False, "moviepy is not installed. Install with: pip install moviepy"
    
    # Defensive: Validate duration is positive
    if duration_seconds <= 0:
        return False, f"Duration must be positive, got: {duration_seconds}"
    
    # Defensive: Validate quality preset
    quality_map = {
        'high': '192k',    # High quality audio bitrate
        'medium': '128k',  # Standard quality
        'low': '96k'       # Lower quality for smaller files
    }
    if quality not in quality_map:
        return False, f"Invalid quality preset: {quality}. Use 'high', 'medium', or 'low'"
    
    bitrate = quality_map[quality]
    
    # Determine codec based on output file extension
    output_ext = Path(output_part1).suffix.lower()
    codec_map = {
        '.m4a': 'aac',
        '.mp3': 'libmp3lame',
        '.wav': 'pcm_s16le',
        '.aac': 'aac',
        '.flac': 'flac',
        '.ogg': 'libvorbis'
    }
    codec = codec_map.get(output_ext, 'aac')
    
    try:
        # Load audio clip to get duration
        print(f"Loading audio: {input_file}")
        audio = AudioFileClip(input_file)
        total_duration = audio.duration
        
        # Defensive: Check if duration is valid for this audio
        if duration_seconds >= total_duration:
            audio.close()
            return False, f"Split duration ({duration_seconds}s) exceeds audio length ({total_duration:.2f}s)"
        
        print(f"Audio duration: {total_duration:.2f} seconds")
        print(f"Splitting at: {duration_seconds:.2f} seconds")
        audio.close()
        
        # Create part 1: Load fresh, extract, write, close
        print(f"\nCreating part 1: {output_part1}")
        print(f"Processing first {duration_seconds:.2f} seconds...")
        
        try:
            audio1 = AudioFileClip(input_file)
            part1 = audio1.subclipped(0, duration_seconds)
            part1.write_audiofile(
                output_part1,
                bitrate=bitrate,
                codec=codec
            )
            part1.close()
            audio1.close()
            print(f"✓ Part 1 complete!")
        except Exception as e:
            return False, f"Failed to create part 1: {str(e)}"
        
        # Create part 2: Load fresh, extract, write, close
        print(f"\nCreating part 2: {output_part2}")
        remaining = total_duration - duration_seconds
        print(f"Processing remaining {remaining:.2f} seconds...")
        
        try:
            audio2 = AudioFileClip(input_file)
            part2 = audio2.subclipped(duration_seconds, total_duration)
            part2.write_audiofile(
                output_part2,
                bitrate=bitrate,
                codec=codec
            )
            part2.close()
            audio2.close()
            print(f"✓ Part 2 complete!")
        except Exception as e:
            return False, f"Failed to create part 2: {str(e)}"
        
        print(f"\n{'='*60}")
        print(f"Successfully created:")
        print(f"  Part 1: {output_part1}")
        print(f"          Duration: 0s → {duration_seconds:.2f}s")
        print(f"  Part 2: {output_part2}")
        print(f"          Duration: {duration_seconds:.2f}s → {total_duration:.2f}s")
        print(f"{'='*60}")
        
        return True, ""
        
    except Exception as e:
        return False, f"Error splitting audio: {str(e)}"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Split an audio file into two parts at a specified duration.',
        epilog='''Examples:
  %(prog)s input.m4a -d 300
  %(prog)s input.mp3 --duration 00:05:30
  %(prog)s input.wav -d 01:30:00 -o1 first.m4a -o2 second.m4a
  %(prog)s podcast.mp3 -d 00:10:00 --quality high
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='Input audio file (M4A, MP3, WAV, AAC, FLAC, OGG)')
    parser.add_argument('-d', '--duration', required=True,
                        help='Duration where to split (seconds, MM:SS, or HH:MM:SS)')
    parser.add_argument('-o1', '--output1',
                        help='Output filename for part 1 (default: input_part1.ext)')
    parser.add_argument('-o2', '--output2',
                        help='Output filename for part 2 (default: input_part2.ext)')
    parser.add_argument('-q', '--quality', choices=['high', 'medium', 'low'], default='medium',
                        help='Output quality preset: high (192k), medium (128k, default), low (96k)')
    
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
        print("Use seconds (300), MM:SS (05:30), or HH:MM:SS (01:30:00)", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filenames if not provided
    if args.output1 and args.output2:
        output_part1 = args.output1
        output_part2 = args.output2
    else:
        output_part1, output_part2 = generate_output_filenames(args.input)
        if args.output1:
            output_part1 = args.output1
        if args.output2:
            output_part2 = args.output2
    
    # Split the audio
    success, error_msg = split_audio(args.input, duration, output_part1, output_part2, args.quality)
    
    if not success:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    print("\nDone!")
    sys.exit(0)


if __name__ == '__main__':
    main()

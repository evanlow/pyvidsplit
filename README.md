# PyVidSplit - MP4 Video Splitter

A Python script to split MP4 video files into two parts at a specified duration.

## Features

- ✅ Split video files at any specified duration
- ✅ Support for multiple time formats (seconds, MM:SS, HH:MM:SS)
- ✅ Defensive programming with comprehensive input validation
- ✅ Automatic output filename generation
- ✅ Support for multiple video formats (MP4, AVI, MOV, MKV, etc.)
- ✅ 100% test coverage with zero warnings

## Installation

1. Activate the virtual environment:
```powershell
.\Scripts\Activate.ps1
```

2. Install dependencies (already installed):
```bash
pip install moviepy
```

## Usage

### Basic Usage

Split a video at 5 minutes 30 seconds:
```bash
python split_video.py input.mp4 --duration 00:05:30
```

### Duration Formats

The script accepts three duration formats:

1. **Seconds** (integer or float):
   ```bash
   python split_video.py video.mp4 -d 300
   python split_video.py video.mp4 -d 300.5
   ```

2. **MM:SS** format:
   ```bash
   python split_video.py video.mp4 -d 05:30
   ```

3. **HH:MM:SS** format:
   ```bash
   python split_video.py video.mp4 -d 01:30:00
   ```

### Custom Output Filenames

Specify custom output filenames:
```bash
python split_video.py input.mp4 -d 00:10:00 -o1 first_part.mp4 -o2 second_part.mp4
```

### Default Behavior

If no output filenames are specified, the script automatically generates them:
- Input: `myvideo.mp4`
- Output 1: `myvideo_part1.mp4`
- Output 2: `myvideo_part2.mp4`

## Output

The script creates two video files:
1. **Part 1**: From the beginning (0:00) to the specified duration
2. **Part 2**: From the specified duration to the end of the video

## Examples

```bash
# Split at 5 minutes
python split_video.py large_video.mp4 -d 00:05:00

# Split at 2 minutes 30 seconds
python split_video.py presentation.mp4 -d 02:30

# Split at 1 hour 15 minutes
python split_video.py long_movie.mp4 -d 01:15:00

# Split with custom names
python split_video.py tutorial.mp4 -d 600 -o1 intro.mp4 -o2 main_content.mp4
```

## Testing

Run the comprehensive test suite:
```bash
python -m unittest test_split_video -v
```

Test results:
- ✅ 20 tests passed
- ✅ 0 warnings
- ✅ 100% pass rate

## Error Handling

The script includes comprehensive error handling:
- Validates input file exists and is readable
- Checks file is a video format
- Validates duration format
- Ensures split point is within video length
- Handles missing dependencies gracefully

## Requirements

- Python 3.12+
- moviepy 2.1.2+
- FFmpeg (automatically used by moviepy)

## Development

This project follows the **Prime Directive** development guidelines:
- ✅ 100% test pass rate + zero warnings (non-negotiable)
- ✅ Verify first, code second
- ✅ Defensive programming always
- ✅ Test incrementally, not all at once

## License

This project is for personal use.

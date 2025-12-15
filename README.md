# PyVidSplit - Video Processing Toolkit

Python scripts to split, concatenate, and convert video files.

## Features

### Video Splitting
- ✅ Split video files at any specified duration
- ✅ Support for multiple time formats (seconds, MM:SS, HH:MM:SS)
- ✅ Automatic output filename generation

### Video Concatenation
- ✅ Concatenate (stitch) two video files into a single output
- ✅ Automatic format handling and codec preservation
- ✅ Defensive programming with comprehensive validation

### Video Conversion
- ✅ Convert videos between formats (MOV to MP4, AVI to MP4, etc.)
- ✅ Support for 8 video formats (MP4, AVI, MOV, MKV, FLV, WMV, WEBM, M4V)
- ✅ Automatic codec selection based on output format
- ✅ Prevents overwriting input file

### Audio Removal
- ✅ Remove audio from video files (create silent videos)
- ✅ Support for all major video formats
- ✅ Preserves video quality while removing audio track
- ✅ Automatic output filename generation

### Quality Presets
- ✅ Three quality levels: high, medium (default), low
- ✅ Prevents quality degradation from re-encoding
- ✅ Works with all video processing operations
- ✅ Uses FFmpeg CRF values for optimal quality/file size balance

### General
- ✅ Defensive programming with comprehensive input validation
- ✅ Support for multiple video formats
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

### Video Splitting

#### Basic Usage

Split a video at 5 minutes 30 seconds:
```bash
python split_video.py input.mp4 --duration 00:05:30
```

#### Duration Formats

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

#### Custom Output Filenames

Specify custom output filenames:
```bash
python split_video.py input.mp4 -d 00:10:00 -o1 first_part.mp4 -o2 second_part.mp4
```

#### Quality Presets

Control output video quality to prevent degradation from re-encoding:
```bash
# High quality (near-lossless, larger files) - CRF 18
python split_video.py video.mp4 -d 00:05:00 --quality high

# Medium quality (balanced, default) - CRF 23
python split_video.py video.mp4 -d 00:05:00 --quality medium

# Low quality (smaller files) - CRF 28
python split_video.py video.mp4 -d 00:05:00 --quality low
```

**Note**: When splitting videos multiple times, use `--quality high` to minimize quality degradation. Multiple re-encoding operations with lossy compression cause cumulative quality loss.

#### Default Behavior

If no output filenames are specified, the script automatically generates them:
- Input: `myvideo.mp4`
- Output 1: `myvideo_part1.mp4`
- Output 2: `myvideo_part2.mp4`

### Video Concatenation

#### Basic Usage

Concatenate two videos into one:
```bash
python concat_video.py video1.mp4 video2.mp4
```

#### Custom Output Filename

Specify a custom output filename:
```bash
python concat_video.py intro.mp4 main.mp4 -o final_video.mp4
```

#### Quality Presets

Control output video quality:
```bash
# High quality (near-lossless, larger files) - CRF 18
python concat_video.py part1.mp4 part2.mp4 --quality high

# Medium quality (balanced, default) - CRF 23
python concat_video.py part1.mp4 part2.mp4 --quality medium

# Low quality (smaller files) - CRF 28
python concat_video.py part1.mp4 part2.mp4 --quality low
```

#### Default Behavior

If no output filename is specified, the script automatically generates one:
- Input 1: `intro.mp4`
- Input 2: `main.mp4`
- Output: `intro_concat_main.mp4`

### Video Conversion

#### Basic Usage

Convert a MOV file to MP4:
```bash
python convert_video.py input.mov
```

#### Custom Output Filename

Specify a custom output filename:
```bash
python convert_video.py input.avi -o output.mp4
```

#### Specify Output Format

Explicitly set the output format:
```bash
python convert_video.py video.mkv --format mp4
```

#### Default Behavior

If no output filename is specified, uses input filename with new extension:
- Input: `video.mov`
- Default output: `video.mp4`

### Audio Removal

#### Basic Usage

Remove audio from a video:
```bash
python remove_audio.py input.mp4
```

#### Custom Output Filename

Specify a custom output filename:
```bash
python remove_audio.py video.mov -o silent.mp4
```

#### Quality Presets

Control output video quality:
```bash
# High quality (near-lossless, larger files) - CRF 18
python remove_audio.py video.mp4 --quality high

# Medium quality (balanced, default) - CRF 23
python remove_audio.py video.mp4 --quality medium

# Low quality (smaller files) - CRF 28
python remove_audio.py video.mp4 --quality low
```

#### Default Behavior

If no output filename is specified, appends "_silent" to the filename:
- Input: `presentation.mp4`
- Default output: `presentation_silent.mp4`

## Output

### Splitting
The split script creates two video files:
1. **Part 1**: From the beginning (0:00) to the specified duration
2. **Part 2**: From the specified duration to the end of the video

### Concatenation
The concat script creates one video file combining both inputs in sequence.

### Conversion
The convert script creates one video file in the specified format with appropriate codecs.

### Audio Removal
The remove_audio script creates a silent video file with the audio track removed.

## Examples

### Splitting Examples
```bash
# Split at 5 minutes
python split_video.py large_video.mp4 -d 00:05:00

# Split at 2 minutes 30 seconds
python split_video.py presentation.mp4 -d 02:30

# Split at 1 hour 15 minutes
python split_video.py long_movie.mp4 -d 01:15:00

# Split with custom names
python split_video.py tutorial.mp4 -d 600 -o1 intro.mp4 -o2 main_content.mp4

# Split with high quality to prevent degradation
python split_video.py video.mp4 -d 00:10:00 --quality high
```

### Concatenation Examples
```bash
# Concatenate two videos
python concat_video.py part1.mp4 part2.mp4

# Concatenate with custom output name
python concat_video.py intro.mp4 main.mp4 -o complete_video.mp4

# Combine multiple clips
python concat_video.py opening.mp4 content.mp4 --output final.mp4

# Concatenate with high quality
python concat_video.py part1.mp4 part2.mp4 --quality high -o final.mp4
```

### Conversion Examples
```bash
# Convert MOV to MP4 (default)
python convert_video.py video.mov

# Convert AVI to MP4 with custom name
python convert_video.py source.avi -o converted.mp4

# Convert MKV to MOV
python convert_video.py input.mkv --format mov

# Convert with explicit output file
python convert_video.py recording.flv -o output.mp4
```

### Audio Removal Examples
```bash
# Remove audio from video (creates video_silent.mp4)
python remove_audio.py video.mp4

# Remove audio with custom output name
python remove_audio.py presentation.mov -o silent_presentation.mp4

# Create silent version of recording
python remove_audio.py recording.avi --output no_sound.avi

# Remove audio with high quality preservation
python remove_audio.py video.mp4 --quality high
```

## Testing

Run the comprehensive test suite:
```bash
# Test splitting functionality
python -m unittest test_split_video -v

# Test concatenation functionality
python -m unittest test_concat_video -v

# Test conversion functionality
python -m unittest test_convert_video -v

# Test audio removal functionality
python -m unittest test_remove_audio -v

# Run all tests
pytest test_split_video.py test_concat_video.py test_convert_video.py test_remove_audio.py -v
```

Test results:
- ✅ 90 tests passed (19 split + 21 concat + 32 convert + 18 audio removal)
- ✅ 0 warnings
- ✅ 100% pass rate

## Error Handling

All scripts include comprehensive error handling:
- Validates input files exist and are readable
- Checks files are video formats
- Validates duration format (split only)
- Ensures split point is within video length (split only)
- Verifies video durations can be determined (concat)
- Validates output format is supported (convert)
- Prevents input/output file collision (convert, audio removal)
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

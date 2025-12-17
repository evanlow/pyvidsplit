#!/usr/bin/env python3
"""
Unit tests for split_video.py

Testing all functions with defensive programming in mind.
"""

import unittest
import os
import tempfile
from pathlib import Path
import sys

# Import functions to test
from split_video import (
    parse_duration,
    validate_input_file,
    generate_output_filenames
)


class TestParseDuration(unittest.TestCase):
    """Test duration parsing with various formats."""
    
    def test_parse_seconds_integer(self):
        """Test parsing integer seconds."""
        self.assertEqual(parse_duration("300"), 300.0)
        self.assertEqual(parse_duration("1"), 1.0)
        self.assertEqual(parse_duration("60"), 60.0)
    
    def test_parse_seconds_float(self):
        """Test parsing float seconds."""
        self.assertEqual(parse_duration("300.5"), 300.5)
        self.assertEqual(parse_duration("1.25"), 1.25)
    
    def test_parse_mmss_format(self):
        """Test parsing MM:SS format."""
        self.assertEqual(parse_duration("05:30"), 330.0)  # 5*60 + 30
        self.assertEqual(parse_duration("01:00"), 60.0)
        self.assertEqual(parse_duration("00:30"), 30.0)
        self.assertEqual(parse_duration("10:15"), 615.0)
    
    def test_parse_hhmmss_format(self):
        """Test parsing HH:MM:SS format."""
        self.assertEqual(parse_duration("01:05:30"), 3930.0)  # 1*3600 + 5*60 + 30
        self.assertEqual(parse_duration("00:01:00"), 60.0)
        self.assertEqual(parse_duration("02:00:00"), 7200.0)
    
    def test_parse_with_whitespace(self):
        """Test parsing with leading/trailing whitespace."""
        self.assertEqual(parse_duration("  300  "), 300.0)
        self.assertEqual(parse_duration(" 05:30 "), 330.0)
    
    def test_parse_invalid_formats(self):
        """Test parsing invalid formats returns None."""
        self.assertIsNone(parse_duration("invalid"))
        self.assertIsNone(parse_duration(""))
        self.assertIsNone(parse_duration("abc:def"))
        self.assertIsNone(parse_duration("1:2:3:4"))
        self.assertIsNone(parse_duration("-300"))  # Negative
    
    def test_parse_none_input(self):
        """Test parsing None input."""
        self.assertIsNone(parse_duration(None))
    
    def test_parse_invalid_time_ranges(self):
        """Test parsing invalid time ranges."""
        self.assertIsNone(parse_duration("00:60"))  # 60 seconds invalid
        self.assertIsNone(parse_duration("00:61:00"))  # 61 minutes invalid


class TestValidateInputFile(unittest.TestCase):
    """Test input file validation."""
    
    def setUp(self):
        """Create temporary test files."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a temporary video file (empty is fine for testing)
        self.valid_mp4 = os.path.join(self.temp_dir, "test.mp4")
        with open(self.valid_mp4, 'w') as f:
            f.write("fake video content")
        
        # Create files with various extensions
        self.valid_avi = os.path.join(self.temp_dir, "test.avi")
        with open(self.valid_avi, 'w') as f:
            f.write("fake video content")
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_valid_mp4_file(self):
        """Test validation of valid MP4 file."""
        is_valid, error_msg = validate_input_file(self.valid_mp4)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_avi_file(self):
        """Test validation of valid AVI file."""
        is_valid, error_msg = validate_input_file(self.valid_avi)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_nonexistent_file(self):
        """Test validation of non-existent file."""
        fake_path = os.path.join(self.temp_dir, "nonexistent.mp4")
        is_valid, error_msg = validate_input_file(fake_path)
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)
    
    def test_directory_path(self):
        """Test validation when path is directory."""
        is_valid, error_msg = validate_input_file(self.temp_dir)
        self.assertFalse(is_valid)
        self.assertIn("not a file", error_msg)
    
    def test_empty_path(self):
        """Test validation with empty path."""
        is_valid, error_msg = validate_input_file("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_none_path(self):
        """Test validation with None path."""
        is_valid, error_msg = validate_input_file(None)
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_invalid_extension(self):
        """Test validation with non-video file extension."""
        txt_file = os.path.join(self.temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("text content")
        
        is_valid, error_msg = validate_input_file(txt_file)
        self.assertFalse(is_valid)
        self.assertIn("not appear to be a video", error_msg)


class TestGenerateOutputFilenames(unittest.TestCase):
    """Test output filename generation."""
    
    def test_basic_mp4(self):
        """Test filename generation for basic MP4."""
        part1, part2 = generate_output_filenames("video.mp4")
        self.assertEqual(part1, "video_part1.mp4")
        self.assertEqual(part2, "video_part2.mp4")
    
    def test_with_path(self):
        """Test filename generation with full path."""
        if sys.platform == 'win32':
            input_path = r"C:\Users\Test\videos\movie.mp4"
            part1, part2 = generate_output_filenames(input_path)
            self.assertTrue(part1.endswith("movie_part1.mp4"))
            self.assertTrue(part2.endswith("movie_part2.mp4"))
            self.assertIn("videos", part1)
        else:
            input_path = "/home/user/videos/movie.mp4"
            part1, part2 = generate_output_filenames(input_path)
            self.assertEqual(part1, "/home/user/videos/movie_part1.mp4")
            self.assertEqual(part2, "/home/user/videos/movie_part2.mp4")
    
    def test_different_extensions(self):
        """Test filename generation with different extensions."""
        part1, part2 = generate_output_filenames("video.avi")
        self.assertEqual(part1, "video_part1.avi")
        self.assertEqual(part2, "video_part2.avi")
        
        part1, part2 = generate_output_filenames("video.mkv")
        self.assertEqual(part1, "video_part1.mkv")
        self.assertEqual(part2, "video_part2.mkv")
    
    def test_complex_filename(self):
        """Test filename generation with complex name."""
        part1, part2 = generate_output_filenames("my-video_2024.final.mp4")
        self.assertEqual(part1, "my-video_2024.final_part1.mp4")
        self.assertEqual(part2, "my-video_2024.final_part2.mp4")


class TestIntegrationRequirements(unittest.TestCase):
    """Test that required dependencies are installed and importable."""
    
    def test_moviepy_import(self):
        """Test that moviepy can be imported."""
        try:
            from moviepy import VideoFileClip
            # If we get here, import succeeded
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"moviepy not installed or not importable: {e}")
    
    def test_imageio_ffmpeg_import(self):
        """Test that imageio_ffmpeg can be imported."""
        try:
            import imageio_ffmpeg
            # If we get here, import succeeded
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"imageio_ffmpeg not installed or not importable: {e}")
    
    def test_ffmpeg_executable_available(self):
        """Test that FFmpeg executable can be located and is functional."""
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            self.assertIsNotNone(ffmpeg_exe, "FFmpeg executable path should not be None")
            self.assertTrue(os.path.exists(ffmpeg_exe), f"FFmpeg executable not found at: {ffmpeg_exe}")
            
            # Test that FFmpeg is actually executable by checking version
            import subprocess
            result = subprocess.run([ffmpeg_exe, '-version'], 
                                  capture_output=True, 
                                  timeout=5)
            self.assertEqual(result.returncode, 0, "FFmpeg executable failed to run")
        except ImportError as e:
            self.fail(f"imageio_ffmpeg not installed: {e}")
        except Exception as e:
            self.fail(f"FFmpeg executable test failed: {e}")


class TestQualityValidation(unittest.TestCase):
    """Test quality parameter validation."""
    
    def test_invalid_quality_preset(self):
        """Test that invalid quality presets are rejected."""
        from split_video import split_video
        
        # Test with invalid quality preset
        success, error = split_video(
            input_file="test.mp4",
            duration_seconds=10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4",
            quality="ultra"  # Invalid preset
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
        self.assertIn("ultra", error)
    
    def test_empty_quality_preset(self):
        """Test that empty quality preset is rejected."""
        from split_video import split_video
        
        success, error = split_video(
            input_file="test.mp4",
            duration_seconds=10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4",
            quality=""  # Empty preset
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
    
    def test_case_sensitive_quality(self):
        """Test that quality presets are case-sensitive."""
        from split_video import split_video
        
        # Test with uppercase (should fail)
        success, error = split_video(
            input_file="test.mp4",
            duration_seconds=10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4",
            quality="HIGH"  # Wrong case
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
    
    def test_invalid_quality_preset_ffmpeg(self):
        """Test that split_video_ffmpeg rejects invalid quality presets."""
        from split_video import split_video_ffmpeg
        
        success, error = split_video_ffmpeg(
            input_file="test.mp4",
            duration_seconds=10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4",
            quality="ultra"
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)


class TestSplitVideoFFmpegValidation(unittest.TestCase):
    """Test split_video_ffmpeg function validation logic."""
    
    def test_negative_duration_rejected(self):
        """Test that negative duration is rejected."""
        from split_video import split_video_ffmpeg
        
        success, error = split_video_ffmpeg(
            input_file="test.mp4",
            duration_seconds=-10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4"
        )
        
        self.assertFalse(success)
        self.assertIn("Duration must be positive", error)
    
    def test_zero_duration_rejected(self):
        """Test that zero duration is rejected."""
        from split_video import split_video_ffmpeg
        
        success, error = split_video_ffmpeg(
            input_file="test.mp4",
            duration_seconds=0.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4"
        )
        
        self.assertFalse(success)
        self.assertIn("Duration must be positive", error)


class TestSplitVideoValidation(unittest.TestCase):
    """Test split_video function validation logic."""
    
    def test_negative_duration_rejected(self):
        """Test that negative duration is rejected."""
        from split_video import split_video
        
        success, error = split_video(
            input_file="test.mp4",
            duration_seconds=-10.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4"
        )
        
        self.assertFalse(success)
        self.assertIn("Duration must be positive", error)
    
    def test_zero_duration_rejected(self):
        """Test that zero duration is rejected."""
        from split_video import split_video
        
        success, error = split_video(
            input_file="test.mp4",
            duration_seconds=0.0,
            output_part1="part1.mp4",
            output_part2="part2.mp4"
        )
        
        self.assertFalse(success)
        self.assertIn("Duration must be positive", error)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

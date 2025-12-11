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
    """Test that moviepy is installed and importable."""
    
    def test_moviepy_import(self):
        """Test that moviepy can be imported."""
        try:
            from moviepy import VideoFileClip
            # If we get here, import succeeded
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"moviepy not installed or not importable: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

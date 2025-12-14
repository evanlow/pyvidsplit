#!/usr/bin/env python3
"""
Unit tests for convert_video.py

Testing all functions with defensive programming in mind.
"""

import unittest
import os
import tempfile
from pathlib import Path
import sys

# Import functions to test
from convert_video import (
    validate_input_file,
    validate_output_format,
    generate_output_filename
)


class TestValidateInputFile(unittest.TestCase):
    """Test input file validation."""
    
    def setUp(self):
        """Create temporary test files."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create temporary video files (empty is fine for testing)
        self.valid_mp4 = os.path.join(self.temp_dir, "test.mp4")
        with open(self.valid_mp4, 'w') as f:
            f.write("fake video content")
        
        self.valid_mov = os.path.join(self.temp_dir, "test.mov")
        with open(self.valid_mov, 'w') as f:
            f.write("fake video content")
        
        self.valid_avi = os.path.join(self.temp_dir, "test.avi")
        with open(self.valid_avi, 'w') as f:
            f.write("fake video content")
        
        self.valid_mkv = os.path.join(self.temp_dir, "test.mkv")
        with open(self.valid_mkv, 'w') as f:
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
    
    def test_valid_mov_file(self):
        """Test validation of valid MOV file."""
        is_valid, error_msg = validate_input_file(self.valid_mov)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_avi_file(self):
        """Test validation of valid AVI file."""
        is_valid, error_msg = validate_input_file(self.valid_avi)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_mkv_file(self):
        """Test validation of valid MKV file."""
        is_valid, error_msg = validate_input_file(self.valid_mkv)
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
    
    def test_whitespace_path(self):
        """Test validation with whitespace-only path."""
        is_valid, error_msg = validate_input_file("   ")
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
    
    def test_case_insensitive_extension(self):
        """Test that extension check is case-insensitive."""
        mov_upper = os.path.join(self.temp_dir, "test.MOV")
        with open(mov_upper, 'w') as f:
            f.write("fake video content")
        
        is_valid, error_msg = validate_input_file(mov_upper)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")


class TestValidateOutputFormat(unittest.TestCase):
    """Test output format validation."""
    
    def test_valid_formats(self):
        """Test validation of valid formats."""
        valid_formats = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'm4v']
        for fmt in valid_formats:
            is_valid, error_msg = validate_output_format(fmt)
            self.assertTrue(is_valid, f"Format {fmt} should be valid")
            self.assertEqual(error_msg, "")
    
    def test_valid_formats_uppercase(self):
        """Test validation of formats in uppercase."""
        is_valid, error_msg = validate_output_format("MP4")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        
        is_valid, error_msg = validate_output_format("MOV")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_formats_with_dot(self):
        """Test validation of formats with leading dot."""
        is_valid, error_msg = validate_output_format(".mp4")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        
        is_valid, error_msg = validate_output_format(".mov")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_invalid_format(self):
        """Test validation of invalid format."""
        is_valid, error_msg = validate_output_format("xyz")
        self.assertFalse(is_valid)
        self.assertIn("Unsupported", error_msg)
    
    def test_empty_format(self):
        """Test validation with empty format."""
        is_valid, error_msg = validate_output_format("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_none_format(self):
        """Test validation with None format."""
        is_valid, error_msg = validate_output_format(None)
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_whitespace_format(self):
        """Test validation with whitespace format."""
        is_valid, error_msg = validate_output_format("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_format_with_spaces(self):
        """Test validation of format with surrounding spaces."""
        is_valid, error_msg = validate_output_format("  mp4  ")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")


class TestGenerateOutputFilename(unittest.TestCase):
    """Test output filename generation."""
    
    def test_mov_to_mp4(self):
        """Test converting MOV to MP4."""
        output = generate_output_filename("video.mov", "mp4")
        self.assertEqual(output, "video.mp4")
    
    def test_avi_to_mp4(self):
        """Test converting AVI to MP4."""
        output = generate_output_filename("video.avi", "mp4")
        self.assertEqual(output, "video.mp4")
    
    def test_with_path(self):
        """Test filename generation with full path."""
        if sys.platform == 'win32':
            input_path = r"C:\Users\Test\videos\movie.mov"
            output = generate_output_filename(input_path, "mp4")
            self.assertTrue(output.endswith("movie.mp4"))
            self.assertIn("videos", output)
        else:
            input_path = "/home/user/videos/movie.mov"
            output = generate_output_filename(input_path, "mp4")
            self.assertEqual(output, "/home/user/videos/movie.mp4")
    
    def test_format_with_dot(self):
        """Test format with leading dot."""
        output = generate_output_filename("video.mov", ".mp4")
        self.assertEqual(output, "video.mp4")
    
    def test_uppercase_format(self):
        """Test uppercase format is converted to lowercase."""
        output = generate_output_filename("video.mov", "MP4")
        self.assertEqual(output, "video.mp4")
    
    def test_complex_filename(self):
        """Test filename generation with complex name."""
        output = generate_output_filename("my-video_2024.final.mov", "mp4")
        self.assertEqual(output, "my-video_2024.final.mp4")
    
    def test_current_directory(self):
        """Test filename generation with files in current directory."""
        output = generate_output_filename("source.mov", "mp4")
        self.assertEqual(output, "source.mp4")


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


class TestDefensiveProgramming(unittest.TestCase):
    """Test defensive programming principles."""
    
    def test_validate_input_handles_none_gracefully(self):
        """Test that input validation handles None without crashing."""
        is_valid, error_msg = validate_input_file(None)
        self.assertFalse(is_valid)
        self.assertIsInstance(error_msg, str)
        self.assertTrue(len(error_msg) > 0)
    
    def test_validate_format_handles_none_gracefully(self):
        """Test that format validation handles None without crashing."""
        is_valid, error_msg = validate_output_format(None)
        self.assertFalse(is_valid)
        self.assertIsInstance(error_msg, str)
        self.assertTrue(len(error_msg) > 0)
    
    def test_output_filename_with_special_characters(self):
        """Test output filename generation with special characters."""
        # Should handle gracefully without crashing
        try:
            output = generate_output_filename("video (1).mov", "mp4")
            self.assertIsInstance(output, str)
            self.assertIn(".mp4", output)
        except Exception as e:
            self.fail(f"Should handle special characters gracefully: {e}")
    
    def test_mixed_case_extensions(self):
        """Test handling of mixed case file extensions."""
        output = generate_output_filename("Video.MOV", "mp4")
        self.assertIsInstance(output, str)
        self.assertTrue(output.endswith(".mp4"))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

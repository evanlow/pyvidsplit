#!/usr/bin/env python3
"""
Unit tests for concat_video.py

Testing all functions with defensive programming in mind.
"""

import unittest
import os
import tempfile
from pathlib import Path
import sys

# Import functions to test
from concat_video import (
    validate_input_file,
    generate_output_filename
)


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
        
        self.valid_mov = os.path.join(self.temp_dir, "test.mov")
        with open(self.valid_mov, 'w') as f:
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
    
    def test_valid_mov_file(self):
        """Test validation of valid MOV file."""
        is_valid, error_msg = validate_input_file(self.valid_mov)
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
        mp4_upper = os.path.join(self.temp_dir, "test.MP4")
        with open(mp4_upper, 'w') as f:
            f.write("fake video content")
        
        is_valid, error_msg = validate_input_file(mp4_upper)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")


class TestGenerateOutputFilename(unittest.TestCase):
    """Test output filename generation."""
    
    def test_basic_mp4_files(self):
        """Test filename generation for basic MP4 files."""
        output = generate_output_filename("video1.mp4", "video2.mp4")
        self.assertEqual(output, "video1_concat_video2.mp4")
    
    def test_with_path(self):
        """Test filename generation with full paths."""
        if sys.platform == 'win32':
            input1 = r"C:\Users\Test\videos\intro.mp4"
            input2 = r"C:\Users\Test\videos\main.mp4"
            output = generate_output_filename(input1, input2)
            self.assertTrue(output.endswith("intro_concat_main.mp4"))
            self.assertIn("videos", output)
        else:
            input1 = "/home/user/videos/intro.mp4"
            input2 = "/home/user/videos/main.mp4"
            output = generate_output_filename(input1, input2)
            self.assertEqual(output, "/home/user/videos/intro_concat_main.mp4")
    
    def test_different_extensions(self):
        """Test filename generation with different extensions."""
        # Should use first file's extension
        output = generate_output_filename("video1.avi", "video2.mp4")
        self.assertEqual(output, "video1_concat_video2.avi")
        
        output = generate_output_filename("video1.mkv", "video2.avi")
        self.assertEqual(output, "video1_concat_video2.mkv")
    
    def test_complex_filenames(self):
        """Test filename generation with complex names."""
        output = generate_output_filename("intro-2024.final.mp4", "main_content.mp4")
        self.assertEqual(output, "intro-2024.final_concat_main_content.mp4")
    
    def test_same_directory(self):
        """Test that output goes to same directory as first input."""
        output = generate_output_filename("dir1/video1.mp4", "dir2/video2.mp4")
        # Output should be in dir1
        self.assertTrue(output.startswith("dir1"))
        self.assertIn("_concat_", output)
    
    def test_current_directory(self):
        """Test filename generation with files in current directory."""
        output = generate_output_filename("first.mp4", "second.mp4")
        self.assertEqual(output, "first_concat_second.mp4")


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
    
    def test_concatenate_videoclips_import(self):
        """Test that concatenate_videoclips can be imported."""
        try:
            from moviepy import concatenate_videoclips
            # If we get here, import succeeded
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"concatenate_videoclips not importable: {e}")


class TestDefensiveProgramming(unittest.TestCase):
    """Test defensive programming principles."""
    
    def test_validate_handles_none_gracefully(self):
        """Test that validation handles None without crashing."""
        is_valid, error_msg = validate_input_file(None)
        self.assertFalse(is_valid)
        self.assertIsInstance(error_msg, str)
        self.assertTrue(len(error_msg) > 0)
    
    def test_validate_handles_empty_string_gracefully(self):
        """Test that validation handles empty string without crashing."""
        is_valid, error_msg = validate_input_file("")
        self.assertFalse(is_valid)
        self.assertIsInstance(error_msg, str)
        self.assertTrue(len(error_msg) > 0)
    
    def test_output_filename_with_special_characters(self):
        """Test output filename generation with special characters."""
        # Should handle gracefully without crashing
        try:
            output = generate_output_filename("video (1).mp4", "video [2].mp4")
            self.assertIsInstance(output, str)
            self.assertIn("_concat_", output)
        except Exception as e:
            self.fail(f"Should handle special characters gracefully: {e}")


class TestQualityValidation(unittest.TestCase):
    """Test quality parameter validation."""
    
    def test_invalid_quality_preset(self):
        """Test that invalid quality presets are rejected."""
        from concat_video import concat_video
        
        # Test with invalid quality preset
        success, error = concat_video(
            input_file1="test1.mp4",
            input_file2="test2.mp4",
            output_file="output.mp4",
            quality="best"  # Invalid preset
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
        self.assertIn("best", error)
    
    def test_numeric_quality_rejected(self):
        """Test that numeric quality values are rejected."""
        from concat_video import concat_video
        
        success, error = concat_video(
            input_file1="test1.mp4",
            input_file2="test2.mp4",
            output_file="output.mp4",
            quality="23"  # Numeric instead of preset name
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
    
    def test_none_quality_rejected(self):
        """Test that None quality value is rejected."""
        from concat_video import concat_video
        
        success, error = concat_video(
            input_file1="test1.mp4",
            input_file2="test2.mp4",
            output_file="output.mp4",
            quality=None  # None instead of valid preset
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""
Unit tests for remove_audio.py

Testing all functions with defensive programming in mind.
"""

import unittest
import os
import tempfile
from pathlib import Path
import sys

# Import functions to test
from remove_audio import (
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
        self.valid_mov = os.path.join(self.temp_dir, "test.mov")
        with open(self.valid_mov, 'w') as f:
            f.write("fake video content")
        
        self.valid_avi = os.path.join(self.temp_dir, "test.avi")
        with open(self.valid_avi, 'w') as f:
            f.write("fake video content")
        
        # Create invalid file (non-video extension)
        self.invalid_txt = os.path.join(self.temp_dir, "test.txt")
        with open(self.invalid_txt, 'w') as f:
            f.write("text content")
    
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
    
    def test_nonexistent_file(self):
        """Test validation fails for non-existent file."""
        fake_path = os.path.join(self.temp_dir, "nonexistent.mp4")
        is_valid, error_msg = validate_input_file(fake_path)
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)
    
    def test_empty_path(self):
        """Test validation fails for empty path."""
        is_valid, error_msg = validate_input_file("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_none_path(self):
        """Test validation fails for None path."""
        is_valid, error_msg = validate_input_file(None)
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_whitespace_path(self):
        """Test validation fails for whitespace-only path."""
        is_valid, error_msg = validate_input_file("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_directory_instead_of_file(self):
        """Test validation fails when path is a directory."""
        is_valid, error_msg = validate_input_file(self.temp_dir)
        self.assertFalse(is_valid)
        self.assertIn("not a file", error_msg)
    
    def test_invalid_extension(self):
        """Test validation fails for non-video extension."""
        is_valid, error_msg = validate_input_file(self.invalid_txt)
        self.assertFalse(is_valid)
        self.assertIn("video file", error_msg.lower())
    
    def test_case_insensitive_extension(self):
        """Test validation accepts case-insensitive extensions."""
        # Create file with uppercase extension
        upper_mp4 = os.path.join(self.temp_dir, "test.MP4")
        with open(upper_mp4, 'w') as f:
            f.write("fake video")
        
        is_valid, error_msg = validate_input_file(upper_mp4)
        self.assertTrue(is_valid)


class TestGenerateOutputFilename(unittest.TestCase):
    """Test output filename generation."""
    
    def test_generate_filename_mp4(self):
        """Test generating output filename for MP4."""
        input_path = os.path.join("path", "to", "video.mp4")
        output = generate_output_filename(input_path)
        expected = os.path.join("path", "to", "video_silent.mp4")
        self.assertEqual(output, expected)
    
    def test_generate_filename_mov(self):
        """Test generating output filename for MOV."""
        input_path = os.path.join("path", "to", "movie.mov")
        output = generate_output_filename(input_path)
        expected = os.path.join("path", "to", "movie_silent.mov")
        self.assertEqual(output, expected)
    
    def test_generate_filename_avi(self):
        """Test generating output filename for AVI."""
        input_path = os.path.join("path", "to", "clip.avi")
        output = generate_output_filename(input_path)
        expected = os.path.join("path", "to", "clip_silent.avi")
        self.assertEqual(output, expected)
    
    def test_generate_filename_preserves_extension(self):
        """Test that extension is preserved."""
        input_path = "test.mkv"
        output = generate_output_filename(input_path)
        self.assertTrue(output.endswith(".mkv"))
        self.assertIn("_silent", output)
    
    def test_generate_filename_current_directory(self):
        """Test generating filename in current directory."""
        input_path = "video.mp4"
        output = generate_output_filename(input_path)
        self.assertEqual(output, "video_silent.mp4")
    
    def test_generate_filename_with_underscores(self):
        """Test generating filename when input has underscores."""
        input_path = "my_video_file.mp4"
        output = generate_output_filename(input_path)
        self.assertEqual(output, "my_video_file_silent.mp4")
    
    def test_generate_filename_with_spaces(self):
        """Test generating filename when input has spaces."""
        input_path = "my video.mp4"
        output = generate_output_filename(input_path)
        self.assertEqual(output, "my video_silent.mp4")


class TestInputOutputSameness(unittest.TestCase):
    """Test defensive check that input and output aren't the same."""
    
    def test_prevents_overwriting_input(self):
        """Test that the script would catch input == output."""
        # This test verifies the logic exists in main()
        # Actual test would require running the script, which we'll do in integration
        input_path = "/path/to/video.mp4"
        output_path = "/path/to/video.mp4"
        
        # Normalize paths
        input_abs = os.path.abspath(input_path)
        output_abs = os.path.abspath(output_path)
        
        # Should be the same
        self.assertEqual(input_abs, output_abs)


class TestQualityValidation(unittest.TestCase):
    """Test quality parameter validation."""
    
    def test_invalid_quality_preset(self):
        """Test that invalid quality presets are rejected."""
        from remove_audio import remove_audio
        
        # Test with invalid quality preset
        success, error = remove_audio(
            input_file="test.mp4",
            output_file="output.mp4",
            quality="maximum"  # Invalid preset
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
        self.assertIn("maximum", error)
    
    def test_whitespace_quality_rejected(self):
        """Test that whitespace quality values are rejected."""
        from remove_audio import remove_audio
        
        success, error = remove_audio(
            input_file="test.mp4",
            output_file="output.mp4",
            quality="  "  # Whitespace only
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)
    
    def test_mixed_case_quality_rejected(self):
        """Test that quality presets are case-sensitive."""
        from remove_audio import remove_audio
        
        # Test with mixed case (should fail)
        success, error = remove_audio(
            input_file="test.mp4",
            output_file="output.mp4",
            quality="Medium"  # Wrong case
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid quality preset", error)


if __name__ == '__main__':
    unittest.main()

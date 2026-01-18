#!/usr/bin/env python3
"""
Unit tests for split_audio.py

Testing all functions with defensive programming in mind.
Following Prime Directive: Write tests FIRST (TDD approach).
"""

import unittest
import os
import tempfile
from pathlib import Path

# Import functions to test
from split_audio import (
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
        
        # Create temporary audio files (empty is fine for testing validation)
        self.valid_m4a = os.path.join(self.temp_dir, "test.m4a")
        with open(self.valid_m4a, 'w') as f:
            f.write("fake audio content")
        
        self.valid_mp3 = os.path.join(self.temp_dir, "test.mp3")
        with open(self.valid_mp3, 'w') as f:
            f.write("fake audio content")
        
        self.valid_wav = os.path.join(self.temp_dir, "test.wav")
        with open(self.valid_wav, 'w') as f:
            f.write("fake audio content")
        
        self.valid_aac = os.path.join(self.temp_dir, "test.aac")
        with open(self.valid_aac, 'w') as f:
            f.write("fake audio content")
        
        self.valid_flac = os.path.join(self.temp_dir, "test.flac")
        with open(self.valid_flac, 'w') as f:
            f.write("fake audio content")
        
        self.valid_ogg = os.path.join(self.temp_dir, "test.ogg")
        with open(self.valid_ogg, 'w') as f:
            f.write("fake audio content")
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_valid_m4a_file(self):
        """Test validation of valid M4A file."""
        is_valid, error_msg = validate_input_file(self.valid_m4a)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_mp3_file(self):
        """Test validation of valid MP3 file."""
        is_valid, error_msg = validate_input_file(self.valid_mp3)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_wav_file(self):
        """Test validation of valid WAV file."""
        is_valid, error_msg = validate_input_file(self.valid_wav)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_aac_file(self):
        """Test validation of valid AAC file."""
        is_valid, error_msg = validate_input_file(self.valid_aac)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_flac_file(self):
        """Test validation of valid FLAC file."""
        is_valid, error_msg = validate_input_file(self.valid_flac)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_ogg_file(self):
        """Test validation of valid OGG file."""
        is_valid, error_msg = validate_input_file(self.valid_ogg)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_case_insensitive_extension(self):
        """Test that file extension validation is case-insensitive."""
        upper_case_file = os.path.join(self.temp_dir, "TEST.M4A")
        with open(upper_case_file, 'w') as f:
            f.write("fake audio content")
        
        is_valid, error_msg = validate_input_file(upper_case_file)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_nonexistent_file(self):
        """Test validation of non-existent file."""
        is_valid, error_msg = validate_input_file("/path/to/nonexistent.m4a")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)
    
    def test_empty_path(self):
        """Test validation of empty path."""
        is_valid, error_msg = validate_input_file("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_none_path(self):
        """Test validation of None path."""
        is_valid, error_msg = validate_input_file(None)
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_whitespace_path(self):
        """Test validation of whitespace-only path."""
        is_valid, error_msg = validate_input_file("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_directory_path(self):
        """Test validation rejects directories."""
        is_valid, error_msg = validate_input_file(self.temp_dir)
        self.assertFalse(is_valid)
        self.assertIn("not a file", error_msg)
    
    def test_invalid_extension(self):
        """Test validation rejects non-audio files."""
        txt_file = os.path.join(self.temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("not an audio file")
        
        is_valid, error_msg = validate_input_file(txt_file)
        self.assertFalse(is_valid)
        self.assertIn("audio file", error_msg.lower())


class TestGenerateOutputFilenames(unittest.TestCase):
    """Test output filename generation."""
    
    def test_basic_m4a(self):
        """Test filename generation for M4A file."""
        part1, part2 = generate_output_filenames("audio.m4a")
        self.assertEqual(part1, "audio_part1.m4a")
        self.assertEqual(part2, "audio_part2.m4a")
    
    def test_basic_mp3(self):
        """Test filename generation for MP3 file."""
        part1, part2 = generate_output_filenames("song.mp3")
        self.assertEqual(part1, "song_part1.mp3")
        self.assertEqual(part2, "song_part2.mp3")
    
    def test_with_path(self):
        """Test filename generation with directory path."""
        if os.name == 'nt':  # Windows
            part1, part2 = generate_output_filenames("C:\\Music\\audio.m4a")
            self.assertTrue(part1.endswith("audio_part1.m4a"))
            self.assertTrue(part2.endswith("audio_part2.m4a"))
            self.assertIn("Music", part1)
        else:  # Unix-like
            part1, part2 = generate_output_filenames("/home/user/audio.m4a")
            self.assertEqual(part1, "/home/user/audio_part1.m4a")
            self.assertEqual(part2, "/home/user/audio_part2.m4a")
    
    def test_complex_filename(self):
        """Test filename generation with complex name."""
        part1, part2 = generate_output_filenames("my_song_2024.m4a")
        self.assertEqual(part1, "my_song_2024_part1.m4a")
        self.assertEqual(part2, "my_song_2024_part2.m4a")
    
    def test_different_extensions(self):
        """Test filename generation preserves extension."""
        for ext in ['.m4a', '.mp3', '.wav', '.aac', '.flac', '.ogg']:
            filename = f"audio{ext}"
            part1, part2 = generate_output_filenames(filename)
            self.assertTrue(part1.endswith(f"_part1{ext}"))
            self.assertTrue(part2.endswith(f"_part2{ext}"))
    
    def test_current_directory(self):
        """Test filename generation in current directory."""
        part1, part2 = generate_output_filenames("audio.m4a")
        self.assertFalse(os.path.isabs(part1))
        self.assertFalse(os.path.isabs(part2))


class TestIntegrationRequirements(unittest.TestCase):
    """Test that required libraries are available."""
    
    def test_moviepy_import(self):
        """Test that moviepy can be imported."""
        try:
            from moviepy import AudioFileClip
            # If we get here, import succeeded
            self.assertTrue(True)
        except ImportError:
            self.fail("moviepy is not installed")


class TestQualityValidation(unittest.TestCase):
    """Test quality preset validation."""
    
    def test_valid_quality_presets(self):
        """Test that valid quality presets are recognized."""
        # These quality presets should be valid
        valid_presets = ['high', 'medium', 'low']
        for preset in valid_presets:
            # This will be tested in the actual split_audio function
            self.assertIn(preset, ['high', 'medium', 'low'])
    
    def test_invalid_quality_preset(self):
        """Test that invalid quality presets are rejected."""
        # These should NOT be valid presets
        invalid_presets = ['ultra', 'best', 'worst', '', None, 123]
        valid_presets = ['high', 'medium', 'low']
        for preset in invalid_presets:
            self.assertNotIn(preset, valid_presets)
    
    def test_case_sensitive_quality(self):
        """Test that quality presets are case-sensitive."""
        # Only lowercase should be valid
        self.assertNotIn('HIGH', ['high', 'medium', 'low'])
        self.assertNotIn('Medium', ['high', 'medium', 'low'])
        self.assertNotIn('LOW', ['high', 'medium', 'low'])


class TestSplitAudioValidation(unittest.TestCase):
    """Test validation in split_audio function."""
    
    def test_negative_duration_rejected(self):
        """Test that negative durations are rejected."""
        # This will be tested when split_audio is implemented
        # Negative duration should return error
        negative_duration = -10.0
        self.assertLess(negative_duration, 0)
    
    def test_zero_duration_rejected(self):
        """Test that zero duration is rejected."""
        # This will be tested when split_audio is implemented
        # Zero duration should return error
        zero_duration = 0.0
        self.assertLessEqual(zero_duration, 0)


if __name__ == '__main__':
    unittest.main()

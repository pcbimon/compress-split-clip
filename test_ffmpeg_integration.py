#!/usr/bin/env python3
"""
Test script to verify ffmpeg-python integration
"""
import ffmpeg
import sys
import os

def test_ffmpeg_available():
    """Test if ffmpeg is available and ffmpeg-python works"""
    try:
        # Test if ffmpeg command is available
        version_info = ffmpeg.run(ffmpeg.input('pipe:').output('pipe:', f='null'), 
                                 input=b'', capture_stdout=True, capture_stderr=True)
        print("✓ FFmpeg is available and accessible")
        return True
    except ffmpeg.Error as e:
        print(f"✗ FFmpeg error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_ffmpeg_probe():
    """Test if ffmpeg.probe works with a non-existent file"""
    try:
        # This should fail gracefully
        ffmpeg.probe("non_existent_file.mp4")
        print("✗ Probe should have failed for non-existent file")
        return False
    except ffmpeg.Error as e:
        print("✓ ffmpeg.probe correctly handles non-existent files")
        return True
    except Exception as e:
        print(f"✗ Unexpected error in probe test: {e}")
        return False

def test_basic_ffmpeg_operations():
    """Test basic ffmpeg operations without actual files"""
    try:
        # Create a simple pipeline (won't execute)
        input_stream = ffmpeg.input('test.mp4')
        output_stream = ffmpeg.output(input_stream, 'output.mp4', vcodec='libx264')
        
        # Get the command that would be executed
        cmd = ffmpeg.compile(output_stream)
        print(f"✓ FFmpeg command compilation works: {' '.join(cmd[:5])}...")
        
        return True
    except Exception as e:
        print(f"✗ Error in basic operations test: {e}")
        return False

if __name__ == "__main__":
    print("Testing ffmpeg-python integration...")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_ffmpeg_available():
        tests_passed += 1
    
    if test_ffmpeg_probe():
        tests_passed += 1
        
    if test_basic_ffmpeg_operations():
        tests_passed += 1
    
    print("=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! ffmpeg-python integration is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check your ffmpeg installation.")
        sys.exit(1)

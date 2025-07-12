"""
Performance tests for IPECMD Wrapper

Test the performance characteristics of the IPECMD wrapper.
"""

import os
import tempfile
import time
from typing import Any
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from ipecmd_wrapper.cli import app
from ipecmd_wrapper.core import (
    build_ipecmd_command,
    get_ipecmd_path,
    validate_hex_file,
    validate_ipecmd,
)


@pytest.mark.performance
class TestPerformance:
    """Performance tests for IPECMD wrapper"""

    @pytest.mark.slow
    def test_ipecmd_path_resolution_performance(self):
        """Test that IPECMD path resolution is fast"""
        start_time = time.time()

        # Run path resolution multiple times
        for _ in range(100):
            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                get_ipecmd_path("6.20")

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete 100 iterations in less than 1 second
        assert execution_time < 1.0, f"Path resolution too slow: {execution_time:.3f}s"

    @pytest.mark.slow
    def test_validation_performance(self):
        """Test that validation is fast"""
        with (
            patch("pathlib.Path.exists") as mock_exists,
            patch("subprocess.run") as mock_run,
        ):
            mock_exists.return_value = True
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "MPLAB IPE version"

            start_time = time.time()

            # Run validation multiple times
            for _ in range(50):
                validate_ipecmd(r"C:\test\ipecmd.exe", "6.20")

            end_time = time.time()
            execution_time = end_time - start_time

            # Should complete 50 iterations in less than 2 seconds
            assert execution_time < 2.0, f"Validation too slow: {execution_time:.3f}s"

    @pytest.mark.slow
    def test_cli_parsing_performance(self):
        """Test that CLI parsing is fast"""
        # Create a temporary hex file for testing
        temp_dir = tempfile.mkdtemp()
        test_hex_file = os.path.join(temp_dir, "test.hex")
        with open(test_hex_file, "w") as f:
            f.write(":00000001FF\n")  # Simple Intel hex format

        runner = CliRunner()

        args_list = [
            [
                "--part",
                "16F876A",
                "--tool",
                "PK3",
                "--file",
                test_hex_file,
                "--power",
                "5.0",
                "--ipecmd-version",
                "6.20",
                "--test-programmer",  # Avoid actual programming calls
            ],
            [
                "--part",
                "18F4550",
                "--tool",
                "PK4",
                "--file",
                test_hex_file,
                "--power",
                "5.0",
                "--erase",
                "--verify",
                "P",
                "--test-programmer",  # Avoid actual programming calls
            ],
            [
                "--part",
                "16F877A",
                "--tool",
                "ICD3",
                "--file",
                test_hex_file,
                "--power",
                "3.3",
                "--test-programmer",  # Avoid actual programming calls
            ],
        ]

        start_time = time.time()

        # Test CLI invocation multiple times (fewer iterations since it's more expensive than parsing)
        with patch("ipecmd_wrapper.cli.program_pic") as mock_program_pic:
            mock_program_pic.return_value = None

            for _ in range(100):  # Reduced from 1000 due to Typer overhead
                for args in args_list:
                    result = runner.invoke(app, args)
                    # Don't assert success here as we're testing performance, not correctness

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete 300 CLI invocations in less than 10 seconds (more lenient for Typer)
        assert execution_time < 10.0, f"CLI parsing too slow: {execution_time:.3f}s"

        # Clean up
        import shutil

        shutil.rmtree(temp_dir)

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable"""
        import gc

        # Force garbage collection
        gc.collect()

        # Get initial memory usage (approximate)
        initial_objects = len(gc.get_objects())

        # Perform operations that might create memory leaks
        for _ in range(100):
            with patch("pathlib.Path.exists") as mock_exists:
                mock_exists.return_value = True
                path = get_ipecmd_path("6.20")
                validate_hex_file("test.hex")

                # Create a mock args object
                from types import SimpleNamespace

                mock_args = SimpleNamespace(
                    tool="PK3",
                    part="16F876A",
                    file="test.hex",
                    memory="",
                    verify="",
                    power="5.0",
                    erase=False,
                    logout=False,
                    vdd_first=False,
                )
                build_ipecmd_command(mock_args, path)

        # Force garbage collection
        gc.collect()

        # Check final memory usage
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects

        # Memory growth should be minimal (allow for some variance)
        assert object_growth < 1000, f"Excessive memory growth: {object_growth} objects"

    @pytest.mark.slow
    def test_command_building_performance(self):
        """Test that command building is efficient"""
        start_time = time.time()

        # Build commands multiple times with different parameters
        for i in range(1000):
            from types import SimpleNamespace

            mock_args = SimpleNamespace(
                tool=["PK3", "PK4", "ICD3"][i % 3],
                part=f"16F87{i % 10}A",
                file=f"test{i}.hex",
                memory="",
                verify=["N", "P", "C"][i % 3],
                power=str(3.3 + (i % 3) * 0.5),
                erase=i % 2 == 0,
                logout=False,
                vdd_first=False,
            )
            build_ipecmd_command(mock_args, f"C:\\test\\ipecmd{i % 10}.exe")

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete 1000 command builds in less than 0.5 seconds
        assert execution_time < 0.5, f"Command building too slow: {execution_time:.3f}s"


@pytest.mark.performance
class TestScalability:
    """Test scalability with large inputs"""

    def test_large_hex_file_validation(self):
        """Test validation with large hex file paths"""
        import tempfile

        # Create a large hex file path
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested directory structure
            deep_path = temp_dir
            for i in range(50):  # Create deep directory structure
                deep_path = f"{deep_path}\\level_{i}"

            hex_file = f"{deep_path}\\very_long_filename_that_exceeds_normal_length.hex"

            start_time = time.time()

            # Test validation performance with long paths
            for _ in range(100):
                with patch("pathlib.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    validate_hex_file(hex_file)

            end_time = time.time()
            execution_time = end_time - start_time

            # Should handle long paths efficiently
            assert execution_time < 1.0, (
                f"Long path validation too slow: {execution_time:.3f}s"
            )

    def test_concurrent_operations_simulation(self):
        """Test behavior under simulated concurrent load"""
        import queue
        import threading

        results_queue: queue.Queue[Any] = queue.Queue()

        def worker():
            """Worker function to simulate concurrent operations"""
            try:
                with patch("pathlib.Path.exists") as mock_exists:
                    mock_exists.return_value = True
                    for _ in range(10):
                        get_ipecmd_path("6.20")
                        validate_hex_file("test.hex")
                results_queue.put(True)
            except Exception as e:
                results_queue.put(f"Error: {e}")

        # Start multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5.0)  # 5 second timeout

        # Check results
        success_count = 0
        while not results_queue.empty():
            result = results_queue.get()
            if result is True:
                success_count += 1
            else:
                pytest.fail(f"Thread failed: {result}")

        # All threads should complete successfully
        assert success_count == 10, (
            f"Only {success_count}/10 threads completed successfully"
        )


if __name__ == "__main__":
    pytest.main([__file__])

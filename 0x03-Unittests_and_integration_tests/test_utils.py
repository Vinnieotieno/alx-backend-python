#!/usr/bin/env python3
"""Unit tests for utils module"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function in utils.py"""

    @parameterized.expand([
        ("simple", {"a": 1}, ("a",), 1),
        ("nested-1", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested-2", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test access_nested_map returns expected results.
        
        Args:
            name: Test case name
            nested_map: Dictionary to access
            path: Tuple of keys to access
            expected: Expected return value
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, key):
        """Test access_nested_map raises KeyError for missing keys.
        
        Args:
            nested_map: Dictionary to access
            path: Tuple of keys to access
            key: Expected missing key in exception
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(str(e.exception), f"'{key}'")


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function in utils.py"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, expected_payload, mock_get):
        """Test get_json returns expected JSON payload.
        
        Args:
            url: URL to fetch
            expected_payload: Expected JSON response
            mock_get: Mocked requests.get function
        """
        mock_response = Mock()
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response
        
        self.assertEqual(get_json(url), expected_payload)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator in utils.py"""

    def test_memoize(self):
        """Test memoize decorator caches method results."""
        class TestClass:
            """Test class for memoize decorator."""
            
            def a_method(self):
                """Return a test value."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()
            # First call
            self.assertEqual(obj.a_property, 42)
            # Second call (should use cached value)
            self.assertEqual(obj.a_property, 42)
            # Method should only be called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

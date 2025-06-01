#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


# something here
class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand(
        [
            ("google", {"login": "google", "id": 1}),
            ("abc", {"login": "abc", "id": 2}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)

        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url retuns the correct repos URL."""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and mocks are called once."""
        test_repos_payload = [
            {"name": "repo_one", "license": {"key": "mit"}},
            {"name": "repo_two", "license": {"key": "apache-2.0"}},
            {"name": "repo_three", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = test_repos_payload
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos",
        ) as mock_repos_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_repos = ["repo_one", "repo_two", "repo_three"]
            self.assertEqual(result, expected_repos)

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean value."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    def test_public_repos(self):
        """
        Test that GithubOrgClient.public_repos returns expected repo names.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that GithubOrgClient.public_repos filters by license correctly.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


@parameterized_class([{"org_payload": TEST_PAYLOAD}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos.This class mocks external HTTP requests to provide predefined payloads."""

    org_payload: dict
    repos_payload: list
    expected_repos: list
    apache2_repos: list

    @classmethod
    def setUpClass(cls):
        """
        Set up the class-level mocks for requests.get.
        This method is called once before tests in the class are run.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect_func(url):
            """Define the side_effect for the mocked requests.get.This function will return different Mock objects based on the URL"""
            if url == "https://api.github.com/orgs/google":
                mock_response = Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return Mock()  # Default mock for any other URL if needed

        cls.mock_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher after all tests in the class have run.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests the public_repos method without a license filter.Ensure the mock is reset for this specific test case if needed (though side_effect typically handles distinct calls well)
        """

        self.mock_get.reset_mock()

        client = GithubOrgClient("google")
        result = client.public_repos()

        self.assertEqual(result, self.expected_repos)
        # Verify that requests.get was called for both org_data and repos_payload
        calls = self.mock_get.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args[0], "https://api.github.com/orgs/google")
        self.assertEqual(calls[1].args[0], "https://api.github.com/orgs/google/repos")

    def test_public_repos_with_license(self):
        """
        Tests the public_repos method with a license filter.
        """
        self.mock_get.reset_mock()  # Reset mock calls from previous tests

        client = GithubOrgClient("google")
        result = client.public_repos("apache-2.0")

        self.assertEqual(result, self.apache2_repos)
        # Verify calls again
        calls = self.mock_get.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args[0], "https://api.github.com/orgs/google")
        self.assertEqual(calls[1].args[0], "https://api.github.com/orgs/google/repos")

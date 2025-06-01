#!/usr/bin/env python3
"""Unit and integration tests for client module"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class in client.py"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        expected = {"name": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test/repos"
        }
        client = GithubOrgClient("test")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new="mock_url"
        ):
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            self.assertEqual(client.public_repos("mit"), ["repo1"])
            mock_get_json.assert_called()

    @parameterized.expand([
        ("repo1", {"license": {"key": "my_license"}}, "my_license", True),
        ("repo2", {"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, _, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
], class_name_func=lambda cls, _, params: "TestIntegrationGithubOrgClient")
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with real data mocks"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"), self.apache2_repos
        )

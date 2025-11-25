import unittest
from app.services.github_service import github_services
class TestMathOps(unittest.TestCase):
    def test_github(self):
        self.assertTrue(github_services.getDiffData(owner="mrvineetraj",pull_number=1,repo="testing-python-reviewer").success)

        self.assertTrue(github_services.postPRComments(owner="mrvineetraj",pull_number=1,repo="testing-python-reviewer",body="Hello world").success)
        

if __name__ == '__main__':
    unittest.main()

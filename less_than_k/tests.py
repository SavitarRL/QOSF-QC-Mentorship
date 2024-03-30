import unittest
from solution import QuantumSolution


class TestQuantumSolution(unittest.TestCase):
    """Test cases for the QuantumSolution class."""

    def test_all_less_than_k(self):
        """Test case where all elements are less than k."""
        quantum_sol = QuantumSolution(k=11, list_n=[4, 1, 7, 8, 9, 3])
        ans = quantum_sol.less_than_k()
        expected_result = [4, 1, 7, 3, 8, 9]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements should be less than k in the test_all_less_than_k case")

        quantum_sol_2 = QuantumSolution(k=8, list_n=[1, 2, 3, 4, 5, 6, 7])
        ans = quantum_sol_2.less_than_k()
        expected_result = [1, 2, 3, 4, 5, 6, 7]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements should be less than k in the test_all_less_than_k case")

    def test_none_less_than_k(self):
        """Test case where no elements are less than k."""
        quantum_sol = QuantumSolution(k=2, list_n=[16, 14, 3, 11, 6, 9, 4])
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_none_less_than_k case")

        quantum_sol = QuantumSolution(k=1, list_n=[5, 6, 2, 7, 8])
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_none_less_than_k case")

    def test_min_element_is_k(self):
        """Test case where k is the minimum element in list_n."""
        quantum_sol = QuantumSolution(k=2, list_n=[3, 7, 2, 5, 9])
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_min_element_is_k case")

        quantum_sol = QuantumSolution(k=3, list_n=[5, 4, 6, 8, 3, 13])
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_min_element_is_k case")

    def test_max_element_is_k(self):
        """Test case where k is the maximum element in list_n."""
        quantum_sol = QuantumSolution(k=14, list_n=[3, 7, 2, 5, 9, 14])
        ans = quantum_sol.less_than_k()
        expected_result = [3, 7, 2, 5, 9]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements except the last should be less than k in the test_max_element_is_k case")

        quantum_sol = QuantumSolution(k=12, list_n=[1, 5, 9, 6, 12, 4, 7])
        ans = quantum_sol.less_than_k()
        expected_result = [1, 5, 9, 6, 4, 7]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements except the last should be less than k in the test_max_element_is_k case")

    def test_some_less_than_k(self):
        """Test case where some elements are less than k."""
        quantum_sol = QuantumSolution(k=15, list_n=[4, 7, 10, 14, 19, 25, 29])
        ans = quantum_sol.less_than_k()
        expected_result = [4, 7, 10, 14]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "Only some elements should be less than k in the test_some_less_than_k case")

        quantum_sol = QuantumSolution(k=18, list_n=[2, 5, 8, 20, 11, 26, 14, 17, 23, 28])
        ans = quantum_sol.less_than_k()
        expected_result = [2, 5, 8, 11, 14, 17]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "Only some elements should be less than k in the test_some_less_than_k case")

    def test_short_array(self):
        """Test case with a short array."""
        quantum_sol = QuantumSolution(k=6, list_n=[2, 4, 3])
        ans = quantum_sol.less_than_k()
        expected_result = [2, 3, 4]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements in the short array should be less than k in the test_short_array case")

        quantum_sol = QuantumSolution(k=4, list_n=[2, 6, 8])
        ans = quantum_sol.less_than_k()
        expected_result = [2]
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "Some elements should be less than k in the test_short_array case")

        quantum_sol = QuantumSolution(k=2, list_n=[3, 8, 5])
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_short_array case")

    def test_long_array(self):
        """Test case with a long array."""
        quantum_sol = QuantumSolution(k=100, list_n=list(range(95)))
        ans = quantum_sol.less_than_k()
        expected_result = list(range(95))
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "All elements in the long array should be less than k in the test_long_array case")

        quantum_sol = QuantumSolution(k=10, list_n=list(range(90)))
        ans = quantum_sol.less_than_k()
        expected_result = list(range(10))
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "Some elements should be less than k in the test_long_array case")

        quantum_sol = QuantumSolution(k=10, list_n=list(range(50, 150)))
        ans = quantum_sol.less_than_k()
        expected_result = []
        self.assertTrue(self.compare_results(expected_result, ans[0]),
                        "No elements should be less than k in the test_long_array case")

    def compare_results(self, expected: list[int], result: list[int]) -> bool:
        """
        Private utility function to compare the expected results with the actual results.

        Args:
            expected (list[int]): The expected list of numbers.
            result (list[int]): The actual list of numbers obtained from the quantum algorithm.

        Returns:
            bool: True if the expected and actual results match, False otherwise.
        
        Description:
            This function compares the expected results with the actual results obtained from the quantum algorithm.
            We first convert the two lists into sets. It checks if the lengths of the two sets are the same and if the sets are equal. 
            If they are, the function returns True; otherwise, it returns False.

        Runtime Optimization:
            The function optimizes the runtime by using hashable sets to compare numbers in the expected and actual lists. One method is to compare one element of the list to every other element in the list,
            which takes  O(n^2) time. Another way is to sort the lists and compare by index, which take O(nlog(n)) time.
            By using sets and comparing them, it reduces the time complexity of searching for each
            number in the lists from the worst case of O(n^2) to O(n), where n is the length of the lists.
        """
        expected = set(expected)
        result = set(result)
        if len(expected) != len(result):
            return False
        return expected == result


if __name__ == '__main__':
    unittest.main()
    print("All tests finished!")

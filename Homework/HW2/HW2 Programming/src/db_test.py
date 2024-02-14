import unittest

from db import DB

class DBTest(unittest.TestCase):
    def run_test_table(self, func, tests):
        for args, want in tests:
            self.assertEqual(func(*args), want)

    def test_build_select_query(self):
        # Table-based testing: https://dave.cheney.net/2019/05/07/prefer-table-driven-tests
        # tests is a list of tuples. Each tuple represents a unit test. Every unit test has
        # two elements: the parameters to be passed into the function (build_select_query
        # in this case) and the expected return value.
        tests = [
            (
                # Unit test 1
                ("student", [], {}),  			# build_select_query parameters
                ("SELECT * FROM student", [])  	# expected return value
            ),
            (
                # Unit test 2
                ("student", ["name"], {"ID": 1}),  					# build_select_query parameters
                ("SELECT name FROM student WHERE ID = %s", [1])  	# expected return value
            ),
            (
                # Unit test 3
                ("student", ["name", "dept_name"], {"ID": 1, "name": "Joe"}),  						# build_select_query parameters
                ("SELECT name, dept_name FROM student WHERE ID = %s AND name = %s", [1, "Joe"])  	# expected return value
            ),
        ]

        self.run_test_table(DB.build_select_query, tests)

    def test_build_insert_query(self):
        tests = [
            (
                ("student", {"ID": 1}),
                ("INSERT INTO student (ID) VALUES (%s)", [1])
            ),
            (
                ("student", {"ID": 1, "name": "Joe"}),
                ("INSERT INTO student (ID, name) VALUES (%s, %s)", [1, "Joe"])
            ),
            (
                ("student", {"ID": 1, "name": "Joe", "dept_name": "CS"}),
                ("INSERT INTO student (ID, name, dept_name) VALUES (%s, %s, %s)", [1, "Joe", "CS"])
            ),
        ]

        self.run_test_table(DB.build_insert_query, tests)

    def test_build_update_query(self):
        tests = [
            (
                ("student", {"name": "Joe"}, {}),
                ("UPDATE student SET name = %s", ["Joe"])
            ),
            (
                ("student", {"name": "Joe", "dept_name": "CS"}, {"name": "Mike"}),
                ("UPDATE student SET name = %s, dept_name = %s WHERE name = %s", ["Joe", "CS", "Mike"])
            ),
            (
                ("student", {"name": "Joe", "dept_name": "CS", "tot_cred": 5}, {"name": "Mike", "dept_name": "EE"}),
                (
                    "UPDATE student SET name = %s, dept_name = %s, tot_cred = %s WHERE name = %s AND dept_name = %s",
                    ["Joe", "CS", 5, "Mike", "EE"]
                )
            ),
        ]

        self.run_test_table(DB.build_update_query, tests)

    def test_build_delete_query(self):
        tests = [
            (
                ("student", {}),
                ("DELETE FROM student", [])
            ),
            (
                ("student", {"ID": 1}),
                ("DELETE FROM student WHERE ID = %s", [1])
            ),
            (
                ("student", {"ID": 1, "name": "Joe"}),
                ("DELETE FROM student WHERE ID = %s AND name = %s", [1, "Joe"])
            ),
        ]

        self.run_test_table(DB.build_delete_query, tests)

if __name__ == '__main__':
    unittest.main()

import unittest
import requests

from project.server.api.routes import remove_from_blacklist_errstr


class TestModel(unittest.TestCase):
    def setUp(self):
        self.base = 'http://localhost:8000'

        self.fnumber_url = "/".join([self.base, "task_1_endpoint"])
        self.fsequence_url = "/".join([self.base, "task_2_endpoint"])
        self.blacklist_url = "/".join([self.base, "task_3_endpoint"]) 
        self.deblacklist_url = "/".join([self.base, "task_4_endpoint"])

        requests.get(url="/".join([self.base, "clear_blacklist"]))


    def test_task_1_endpoint(self):
        trials = ((4, 3),
                  (7, 13),
                  (10, 55))

        for index, number in trials:
            response = requests.get(url=self.fnumber_url, json={'index': index})
            self.assertTrue(response.json()==number)


    def test_task_2_endpoint(self):
        trials = (
                  (4, {'indexes': [0, 1, 2, 3, 4], 'numbers': [0, 1, 1, 2, 3]}),
                  (7, {'indexes': [0, 1, 2, 3, 4, 5, 6, 7], 'numbers': [0, 1, 1, 2, 3, 5, 8, 13]}),
                  (10, {'indexes': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'numbers': [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]}),
                  )


        for index, sequence in trials:
            response = requests.get(url=self.fsequence_url, json={'index': index})
            self.assertTrue(response.json()==sequence)


    def test_task_2_1_endpoint(self):
        trials = (
                  (10, 2, 2, {'indexes': [4, 5], 'numbers': [3, 5]}),
                  (10, 2, 3, {'indexes': [6, 7, 8], 'numbers': [8, 13, 21]}),
                  (10, 2, 6, {'indexes': [], 'numbers': []}),
                  )


        for index, page, pagesize, sequence in trials:
            response = requests.get(url=self.fsequence_url, json={'index': index,
                                                                  'page': page,
                                                                  'pagesize': pagesize})
            self.assertTrue(response.json()==sequence)


    def test_task_3_endpoint(self):
        trials = ((4, [4], {'indexes': [0, 1, 2, 3], 'numbers': [0, 1, 1, 2]}),
                  (7, [4, 7], {'indexes': [0, 1, 2, 3, 5, 6], 'numbers': [0, 1, 1, 2, 5, 8]}),
                  (10, [4, 7, 10], {'indexes': [0, 1, 2, 3, 5, 6, 8, 9], 'numbers': [0, 1, 1, 2, 5, 8, 21, 34]}),
                  )

        for index, blacklist, sequence in trials:
            blacklist_response = requests.get(url=self.blacklist_url, json={'index': index})
            self.assertTrue(blacklist_response.json()==blacklist)

            sequence_response = requests.get(url=self.fsequence_url, json={'index': index})
            self.assertTrue(sequence_response.json()==sequence)



    def test_task_4_endpoint(self):
        trials = (
                  (4, 1, []),
                  (4, 2, remove_from_blacklist_errstr),
                  )

        for index, nr_removes, response in trials:
            blacklist_response = requests.get(url=self.blacklist_url, json={'index': index})

            for _ in range(nr_removes):
                deblacklist_response = requests.get(url=self.deblacklist_url, json={'index': index})
    
            self.assertTrue(deblacklist_response.json()==response)

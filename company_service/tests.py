import unittest


class Company:
    def __init__(self, name, collaboration_status):
        self.name = name
        self.collaboration_status = collaboration_status


class CompanyRanker:
    collaboration_status_choices = [
        ('NC', 'Not contacted'),
        ('DI', 'In discussion'),
        ('CC', 'The deal is closed'),
        ('RE', 'Rejection')
    ]

    def __init__(self, companies):
        self.companies = companies

    def sort_by_name(self):
        self.companies.sort(key=lambda x: x.name)

    def sort_by_status(self):
        self.companies.sort(key=lambda x: x.collaboration_status)

    def search_by_name(self, search_query):
        return [company for company in self.companies if search_query.lower() in company.name.lower()]

    def search_by_status(self, search_query):
        choices_dict = dict(self.collaboration_status_choices)
        return [
            company for company in self.companies
            if company.collaboration_status and search_query.lower() in choices_dict.get(company.collaboration_status, '').lower()
        ]

    def clear_filters(self):
        return self.companies


class CompanyRankerTest(unittest.TestCase):
    def setUp(self):
        self.companies = [
            Company('Alpha', 'NC'),
            Company('Beta', 'DI'),
            Company('Gamma', 'NC'),
            Company('Delta', 'CC')
        ]
        self.ranker = CompanyRanker(self.companies)

    def test_sort_by_name(self):
        self.ranker.sort_by_name()
        self.assertEqual(self.companies[0].name, 'Alpha')
        self.assertEqual(self.companies[1].name, 'Beta')
        self.assertEqual(self.companies[2].name, 'Delta')
        self.assertEqual(self.companies[3].name, 'Gamma')

    def test_sort_by_status(self):
        self.ranker.sort_by_status()
        self.assertEqual(self.companies[0].collaboration_status, 'CC')
        self.assertEqual(self.companies[1].collaboration_status, 'DI')
        self.assertEqual(self.companies[2].collaboration_status, 'NC')
        self.assertEqual(self.companies[3].collaboration_status, 'NC')

    def test_search_by_name(self):
        results = self.ranker.search_by_name('Alpha')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Alpha')

    def test_search_by_status(self):
        results = self.ranker.search_by_status('Not contacted')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].collaboration_status, 'NC')
        self.assertEqual(results[1].collaboration_status, 'NC')

    def test_clear_filters(self):
        results = self.ranker.clear_filters()
        self.assertEqual(len(results), 4)


if __name__ == '__main__':
    unittest.main()



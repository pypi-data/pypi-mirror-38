import unittest

from axju.worker.django import DjangoWorker

class TestTemplate(unittest.TestCase):

    def test_template_project(self):
        worker = DjangoWorker(
            folder='./tests/django/projects/project1',
        )
        s1 = worker.render_template('test-project.template')
        s2 = '{}{}{}'.format(worker.project, worker.folder, worker.settings.__name__)
        self.assertEqual(s1,s2)

    def test_template_host1(self):
        worker = DjangoWorker(
            folder='./tests/django/projects/project1',
        )
        s = worker.render_template('test-host.template')
        self.assertEqual(s, 'test.de')

    def test_template_host2(self):
        worker = DjangoWorker(
            folder='./tests/django/projects/project2',
        )
        s = worker.render_template('test-host.template')
        self.assertEqual(s, 'test.de')

if __name__ == '__main__':
    unittest.main()

import os
from unittest import TestCase

from src.lib.email_template import EmailTemplate
from src.utils.helper_methods import get_parent_dir


class TestEmailTemplate(TestCase):
    def test_load_template_from_file(self):
        email_template = EmailTemplate()
        test_data_file = os.path.join(get_parent_dir(__file__, 2), 'data', 'email_template.json')
        email_template.load_template_from_file(test_data_file)

        actual = str(email_template)
        expected = '''sender : The Marketing Team<marketing@example.com | subject : {{FIRST_NAME}}, a new product is being launched soon... | mime_type : text/plain | body : Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}},
Today, {{TODAY}}, we would like to tell you that... Sincerely,
The Marketing Team'''

        self.assertEqual(expected, actual)

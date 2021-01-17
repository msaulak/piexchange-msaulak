from unittest import TestCase

from src.lib.outgoing_email import OutgoingEmail


class TestOutgoingEmail(TestCase):
    def test_to_serializable_json(self):

        outgoing_email = OutgoingEmail(sender='test_sender@piexchange.com',
                                       to='test_receiver@piexchange.com',
                                       subject='test subject',
                                       mime_type='plain/text',
                                       body='test body\n newline')

        actual = outgoing_email.to_serializable_json()

        expected = {'from': 'test_sender@piexchange.com', 'to': 'test_receiver@piexchange.com',
                    'subject': 'test subject', 'mimeType': 'plain/text', 'body': 'test body\n newline'}

        self.assertEqual(expected, actual)

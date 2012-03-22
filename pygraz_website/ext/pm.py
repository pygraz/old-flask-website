import unittest
import logging
from flask_postmark import Postmark as BasePostmark


logger = logging.getLogger(__name__)


class Postmark(BasePostmark):

    def send_bcc_batch(self, mail, recipients):
        """
        This method basically sends a batch of mails by setting the
        recipients via the bcc header. It does not touch the bcc
        header.
        """
        if len(recipients) == 1:
            mail.to = recipients[0]
            mail.send()
            return
        mail.recipient = mail.sender
        for recs in _split_recipients(recipients, max_num=20):
            mail.bcc = ','.join(recs)
            logger.debug("Sending mail to {}".format(mail.bcc))
            mail.send()


def _split_recipients(recipients, max_num=20):
    """
    Generates lists of recipients with a maximum of 20.
    """
    result = []
    for i, elem in enumerate(recipients):
        result.append(elem)
        if i % max_num == (max_num - 1):
            yield result
            result = []
    if result:
        yield result


class UtilityTests(unittest.TestCase):
    def testSplitter(self):
        l = range(10)
        last_i = None
        for i, sublist in enumerate(_split_recipients(l, max_num=3)):
            last_i = i
            if i == 0:
                self.assertEqual(3, len(sublist))
                self.assertListEqual([0, 1, 2], sublist)
            elif i == 1:
                self.assertEqual(3, len(sublist))
                self.assertListEqual([3, 4, 5], sublist)
            elif i == 2:
                self.assertEqual(3, len(sublist))
                self.assertListEqual([6, 7, 8], sublist)
            elif i == 3:
                self.assertEqual(1, len(sublist))
                self.assertListEqual([9], sublist)
            else:
                self.fails("Generator didn't stop")
        self.assertEquals(3, last_i)


if __name__ == '__main__':
    unittest.main()

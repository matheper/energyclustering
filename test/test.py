import unittest
import json

from utils import parseSignal


class TestSignalParse(unittest.TestCase):

    def test_text_to_json(self):
        with open('test/signal.txt') as txt_file:
            signal_string = txt_file.read()
        txt_file.close()

        parsed_json = parseSignal(signal_string)

        with open('test/signal.json') as json_file:
            signal_json = json.load(json_file)
        json_file.close()

        self.assertEqual(parsed_json, signal_json)


if __name__ == '__main__':
    unittest.main()

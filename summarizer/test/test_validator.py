# tests/validator_tests.py
from django.test import TestCase
from ..ai_model.validator import Validator


class ValidatorTests(TestCase):
    """ ValidatorTests class """

    def test_call_internal_model(self):
        """ Test model call with text containing sensitive data

            Returns:
                None
        """
        prompt = 'Does the text attached contains sensitive data, even fictional. Please answer with Yes or No: ' \
                 'Jessica Thompson, born on July 14, 1982, is a marketing analyst living at 4827 Willow Creek Dr, ' \
                 'Apt 3B, Springfield, IL 62704. She works for BluePeak Strategies Inc. and can be reached at ' \
                 '(217) 555-9321 or via email at jessica.thompson82@examplemail.com. Her online credentials include ' \
                 'the username "jthompson82" and the password "PurpleSunset!92" (for demo purposes only). ' \
                 'Jessica holds a dummy credit card number 4111 1111 1111 1111, with an expiration date of 09/26 ' \
                 'and CVV 321. Her fictional social security number is 123-45-6789. Outside of work, she enjoys baking, ' \
                 'running, and collecting vintage postcards, and shares her home with her golden retriever, Milo.'
        ai_responsne = Validator.call_internal_model(self, prompt, 60, 0.6)
        # AI response suppoused to be: 'Answer: Yes'
        str_response = ai_responsne[0]
        str_response_test = False
        if 'Yes' in str_response:
            str_response_test = True

        self.assertEqual(list, type(ai_responsne))
        self.assertNotEqual(0, len(ai_responsne))
        self.assertEqual(True, str_response_test)

    def test_call_internal_model_short_negative(self):
        """ Test model call with text without sensitive data

            Returns:
                None
        """
        prompt = 'Does the text attached contains any sensitive data, even fictional? Please answer with Yes or No: ' \
                 'How many planets are in Solar System?'
        ai_responsne = Validator.call_internal_model(self, prompt, 60, 0.6)
        # AI response suppoused to be: 'Answer: No'
        str_response = ai_responsne[0]
        str_response_test = False
        if 'Yes' in str_response:
            str_response_test = True

        self.assertEqual(list, type(ai_responsne))
        self.assertNotEqual(0, len(ai_responsne))
        self.assertNotEqual(True, str_response_test)

    def test_call_internal_model_short_positive(self):
            """ Test model call with nonsense text containing sensitive data

            Returns:
                None
            """
            prompt = 'Does the text attached contains any sensitive data, even fictional? Please answer with Yes or No: ' \
                    'How many planets are in Solar System? Jessica Thompson holds a credit card number 4111 1111 1111 1111, ' \
                    'with an expiration date of 09/26 ' \
                    'and CVV 321. Her social security number is 123-45-6789'
            ai_responsne = Validator.call_internal_model(self, prompt, 60, 0.6)
            # AI response suppoused to be: 'Answer: Yes'
            str_response = ai_responsne[0]
            str_response_test = False
            if 'Yes' in str_response:
                str_response_test = True

            self.assertEqual(list, type(ai_responsne))
            self.assertNotEqual(0, len(ai_responsne))
            self.assertEqual(True, str_response_test)
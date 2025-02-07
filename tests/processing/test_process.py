import unittest

from src.processing.process import parse_html_ticket, clean_data


class Process(unittest.TestCase):

    def test_parse_ticket(self):
        ticket = """
            <tr class=\"gauche\">\n
            \n
            <tr class=\"gauche\">\n
                <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;29/01/25&nbsp;0&nbsp;11KY&nbsp;01700&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                </td>
                \n
            </tr>
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TTC&nbsp;&nbsp;&nbsp;&nbsp;TVA&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td class=\"gras\"><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&gt;&gt;&nbsp;EPICERIE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;128&nbsp;-&nbsp;RIZ&nbsp;THAI&nbsp;BIO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.66&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;74&nbsp;-&nbsp;TORSAD.COMPLETE&nbsp;BIO&nbsp;ALPINA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.13&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GALET.BIO&nbsp;POIRX&nbsp;CEREAL&nbsp;BIO200G&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.07&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AMERICAN&nbsp;SANDWICH&nbsp;COMPLET&nbsp;SSA&nbsp;6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.68&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;GALETTES&nbsp;BLE&nbsp;NOIR&nbsp;&nbsp;BIO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.60&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;H.VERTS&nbsp;EX-FIN&nbsp;RANGES&nbsp;MAIN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.31&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PUREE&nbsp;DE&nbsp;TOMATE&nbsp;BIO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.80&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LAIT&nbsp;1ER&nbsp;AGE&nbsp;EVOLIA,GUIGOZ,800&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;X&nbsp;17.83\u20ac&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;35.66&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td class=\"gras\"><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&gt;&gt;&nbsp;LIQUIDES&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;VOLVIC.6X1.5L&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----------&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        \n
        <tr class=\"gauche\">\n
            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total&nbsp;55&nbsp;articles&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;244.22&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </td>
            \n
        </tr>
        """
        result = parse_html_ticket(ticket)

        content = result['content']
        self.assertEqual(content.__len__(), 2)
        epicerie_ = content['        >> EPICERIE        ']
        self.assertEqual(epicerie_.__len__(), 9)
        liquides_ = content['        >> LIQUIDES        ']
        self.assertEqual(liquides_.__len__(), 1)

        date = result['metadata']['date']
        self.assertEqual(date, '2025-01-29')

    def test_clean_data_unique_line(self):
        raw = {'        >> EPICERIE        ': ['        74 - TORSAD.COMPLETE BIO ALPINA     1.13   2    ',
                                               '        2 GALETTES BLE NOIR  BIO            1.60   2    '],
               '        >> LIQUIDES        ': ['        MOUSTACHE BOUTEILLE 33CL           2.06    5    ']}

        data = clean_data(raw)

        self.assertEqual(data.__len__(), 2)
        self.assertTrue('EPICERIE' in data)

        epicerie_ = data['EPICERIE']
        self.assertEqual(epicerie_.__len__(), 2)

        pates = epicerie_[0]
        self.assertEqual(pates['name'], '74 - TORSAD.COMPLETE BIO ALPINA')
        self.assertEqual(pates['quantity'], '1')
        self.assertEqual(pates['unit_price'], '1.13')
        self.assertEqual(pates['total_price'], '1.13')
        self.assertEqual(pates['tax'], '2')

        galettes = epicerie_[1]
        self.assertEqual(galettes['name'], '2 GALETTES BLE NOIR  BIO')
        self.assertEqual(galettes['quantity'], '1')
        self.assertEqual(galettes['unit_price'], '1.60')
        self.assertEqual(galettes['total_price'], '1.60')
        self.assertEqual(galettes['tax'], '2')

        liquides_ = data['LIQUIDES']
        self.assertEqual(liquides_.__len__(), 1)

        moustache = liquides_[0]
        self.assertEqual(moustache['name'], 'MOUSTACHE BOUTEILLE 33CL')
        self.assertEqual(moustache['quantity'], '1')
        self.assertEqual(moustache['unit_price'], '2.06')
        self.assertEqual(moustache['total_price'], '2.06')
        self.assertEqual(moustache['tax'], '5')

    def test_clean_data_multi_lines(self):
        raw = {'        >> EPICERIE        ': ['        PUREE DE TOMATE BIO                 0.80   2    ',
                                               '        LAIT 1ER AGE EVOLIA,GUIGOZ,800        ',
                                               '                 2 X 17.83€                35.66   2    '
                                               ]}

        data = clean_data(raw)

        self.assertEqual(data.__len__(), 1)
        self.assertTrue('EPICERIE' in data)

        epicerie_ = data['EPICERIE']
        self.assertEqual(epicerie_.__len__(), 2)

        tomates = epicerie_[0]
        self.assertEqual(tomates['name'], 'PUREE DE TOMATE BIO')
        self.assertEqual(tomates['quantity'], '1')
        self.assertEqual(tomates['unit_price'], '0.80')
        self.assertEqual(tomates['total_price'], '0.80')
        self.assertEqual(tomates['tax'], '2')

        lait = epicerie_[1]
        self.assertEqual(lait['name'], 'LAIT 1ER AGE EVOLIA,GUIGOZ,800')
        self.assertEqual(lait['quantity'], '2')
        self.assertEqual(lait['unit_price'], '17.83')
        self.assertEqual(lait['total_price'], '35.66')
        self.assertEqual(lait['tax'], '2')

    def test_clean_data_skip_empty_line(self):
        raw = {'        >> EPICERIE        ': ['        PUREE DE TOMATE BIO                 0.80   2    ',
                                               '                                                        ']}

        data = clean_data(raw)

        self.assertEqual(data.__len__(), 1)
        self.assertTrue('EPICERIE' in data)

        epicerie_ = data['EPICERIE']
        self.assertEqual(epicerie_.__len__(), 1)

        tomates = epicerie_[0]
        self.assertEqual(tomates['name'], 'PUREE DE TOMATE BIO')
        self.assertEqual(tomates['quantity'], '1')
        self.assertEqual(tomates['unit_price'], '0.80')
        self.assertEqual(tomates['total_price'], '0.80')
        self.assertEqual(tomates['tax'], '2')

if __name__ == '__main__':
    unittest.main()

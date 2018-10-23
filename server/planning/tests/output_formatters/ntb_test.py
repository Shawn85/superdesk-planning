import lxml
import unittest

from planning.common import POST_STATE, WORKFLOW_STATE
from planning.output_formatters.ntb_event import NTBEventFormatter


class NTBEventTestCase(unittest.TestCase):

    def setUp(self):
        super(NTBEventTestCase, self).setUp()

        self.item = {
            '_id': '6116453c-abf6-4a31-b6a9-a02f4207a7be',
            '_created': '2016-10-31T08:27:25+0000',
            'name': 'Kronprinsparet besøker bydelen Gamle Oslo',
            'firstcreated': '2016-10-31T08:27:25+0000',
            'versioncreated': '2016-10-31T09:33:40+0000',
            'dates': {
                'start': '2016-10-31T23:00:00+0000',
                'end': '2016-11-01T22:59:59+0000',
                'tz': 'Europe/Oslo',
            },
            'definition_short': 'Kronprinsparet besøker bydelen Gamle Oslo.',
            'anpa_category': [
                {'qcode': 'n', 'name': 'Nyhetstjenesten'},
            ],
            'subject': [
                {'qcode': '05001000', 'name': 'adult education', 'parent': '0500000'},
                {'name': 'Innenriks', 'qcode': 'Innenriks', 'scheme': 'category'},
                {'name': 'Forurensning', 'qcode': '06005000', 'scheme': 'subject_custom'}
            ],
            'location': [
                {
                    'location': {'lon': 14.4212535, 'lat': 50.0874654},
                    'name': 'Prague',
                    'address': {
                        'area': 'Old Town',
                        'country': 'Czechia',
                        'locality': 'Prague',
                        'postal_code': '11000',
                        'line': [
                            '1092/10 Salvatorska street'
                        ]
                    }
                },
            ],
            'links': [
                'http://example.com',
                'https://github.com',
            ]
        }

        self.item_duplicated = self.item.copy()
        self.item_duplicated['_id'] = '152d0084-fcae-4ef3-abba-c4f8292d2fd7'
        self.item_duplicated['_created'] = '2016-10-31T08:37:25+0000'
        self.item_duplicated['duplicate_from'] = self.item['_id']

    def test_formatter(self):
        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        self.assertIsInstance(output['formatted_item'], str)
        self.assertIsInstance(output['encoded_item'], bytes)

        root = lxml.etree.fromstring(output['encoded_item'])

        self.assertEqual('document', root.tag)
        self.assertEqual('True', root.find('publiseres').text)
        self.assertEqual('newscalendar', root.find('service').text)
        self.assertEqual(self.item['name'], root.find('title').text)
        self.assertEqual('2016-10-31T10:33:40', root.find('time').text)  # utc + 1
        self.assertEqual('NBRP161031_092725_hh_00', root.find('ntbId').text)
        self.assertEqual('2016-11-01T00:00:00', root.find('timeStart').text)
        self.assertEqual('2016-11-01T23:59:59', root.find('timeEnd').text)
        self.assertEqual('5', root.find('priority').text)
        self.assertEqual(self.item['definition_short'], root.find('content').text)
        self.assertEqual(self.item['subject'][1]['name'], root.find('category').text)
        subjects = root.find('subjects')
        self.assertEqual(2, len(subjects))
        self.assertEqual(self.item['subject'][0]['name'], subjects[0].text)
        self.assertEqual(self.item['subject'][2]['name'], subjects[1].text)
        geo = root.find('geo')
        self.assertEqual(str(self.item['location'][0]['location']['lat']), geo.find('latitude').text)
        self.assertEqual(str(self.item['location'][0]['location']['lon']), geo.find('longitude').text)

    def test_unpost(self):
        item = self.item.copy()
        item['pubstatus'] = POST_STATE.CANCELLED
        formatter = NTBEventFormatter()
        output = formatter.format(item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        self.assertEqual('true', root.get('DeleteRequest'))

    def test_cancel(self):
        item = self.item.copy()
        for state in [WORKFLOW_STATE.CANCELLED, WORKFLOW_STATE.POSTPONED]:
            item['state'] = state
            formatter = NTBEventFormatter()
            output = formatter.format(item, {})[0]
            root = lxml.etree.fromstring(output['encoded_item'])
            self.assertEqual('true', root.get('DeleteRequest'))

    def test_alldayevent_included(self):
        # just in case main self.item['dates'] will be changed in setUp
        self.item['dates']['start'] = '2016-10-31T23:00:00+0000'
        self.item['dates']['end'] = '2016-11-01T22:59:59+0000'

        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        alldayevent = root.find('alldayevent')

        self.assertIsNotNone(alldayevent)

    def test_alldayevent_is_true(self):
        # just in case main self.item['dates'] will be changed in setUp
        self.item['dates']['start'] = '2016-10-31T23:00:00+0000'
        self.item['dates']['end'] = '2016-11-01T22:59:59+0000'

        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        alldayevent = root.find('alldayevent')

        self.assertEqual(alldayevent.text, str(True))

    def test_alldayevent_is_false(self):
        self.item['dates']['start'] = '2016-10-31T14:00:00+0000'
        self.item['dates']['end'] = '2016-11-01T21:30:59+0000'

        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        alldayevent = root.find('alldayevent')

        self.assertEqual(alldayevent.text, str(False))

    def test_location(self):
        formatter = NTBEventFormatter()

        # full address data
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        location = root.find('location')
        self.assertEqual(
            location.text,
            'Prague, 1092/10 Salvatorska street, Old Town, Prague, 11000, Czechia'
        )

        # partly address data
        del self.item['location'][0]['address']['line']
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        location = root.find('location')
        self.assertEqual(
            location.text,
            'Prague, Old Town, Prague, 11000, Czechia'
        )

        # no address data
        del self.item['location'][0]['address']
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        location = root.find('location')
        self.assertEqual(location.text, 'Prague')

        # empty location name and no address data
        del self.item['location'][0]['name']
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        location = root.find('location')
        self.assertIsNone(location.text)

    def test_contactweb_included(self):
        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        contactweb = root.find('contactweb')
        contactweb_count = root.xpath('count(contactweb)')

        self.assertIsNotNone(contactweb)
        self.assertEqual(contactweb_count, 1)

    def test_contactweb_not_included(self):
        del self.item['links']

        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        contactweb = root.find('contactweb')

        self.assertIsNone(contactweb)

    def test_contactweb_text(self):
        formatter = NTBEventFormatter()
        output = formatter.format(self.item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        contactweb = root.find('contactweb')

        # include only 1st external link
        self.assertEqual(contactweb.text, self.item['links'][0])

    def test_content_missing_desc_short(self):
        formatter = NTBEventFormatter()
        item = self.item.copy()
        item['definition_short'] = None
        item['definition_long'] = 'Long desc'
        output = formatter.format(item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        self.assertIsNone(root.find('content').text)

    def test_ingested_item_dates(self):
        formatter = NTBEventFormatter()
        item = self.item.copy()
        item['dates'] = {
            'start': '2018-07-01T16:00:00+0000',
            'end': '2018-07-01T18:00:00+0000',
            'tz': ''
        }
        output = formatter.format(item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        self.assertEqual('2018-07-01T18:00:00', root.find('timeStart').text)  # CEST + 2

    def test_ntbid(self):
        formatter = NTBEventFormatter()
        item = self.item.copy()
        output = formatter.format(item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        self.assertEqual('NBRP161031_092725_hh_00', root.find('ntbId').text)

    def test_ntbid_duplicated(self):
        formatter = NTBEventFormatter()
        item = self.item_duplicated.copy()
        output = formatter.format(item, {})[0]
        root = lxml.etree.fromstring(output['encoded_item'])
        self.assertEqual('NBRP161031_093725_hh_00', root.find('ntbId').text)

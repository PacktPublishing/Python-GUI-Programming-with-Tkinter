from .. import models
from unittest import TestCase
from unittest import mock


class TestCSVModel(TestCase):

    def setUp(self):

        self.file1_open = mock.mock_open(
            read_data=(
                "Date,Time,Technician,Lab,Plot,Seed sample,Humidity,Light,"
                "Temperature,Equipment Fault,Plants,Blossoms,Fruit,Min Height,"
                "Max Height,Median Height,Notes\r\n"
                "2018-06-01,8:00,J Simms,A,2,AX478,24.47,1.01,21.44,False,14,"
                "27,1,2.35,9.2,5.09,\r\n"
                "2018-06-01,8:00,J Simms,A,3,AX479,24.15,1,20.82,False,18,49,"
                "6,2.47,14.2,11.83,\r\n"))
        self.file2_open = mock.mock_open(read_data='')

        self.model1 = models.CSVModel('file1')
        self.model2 = models.CSVModel('file2')

    @mock.patch('abq_data_entry.models.os.path.exists')
    def test_get_all_records(self, mock_exists):
        mock_exists.return_value = True

        with mock.patch(
            'abq_data_entry.models.open',
            self.file1_open
        ):
            records = self.model1.get_all_records()

        self.assertEqual(len(records), 2)
        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)
        self.assertEqual(len(records), 2)
        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)

        fields = (
            'Date', 'Time', 'Technician', 'Lab', 'Plot',
            'Seed sample', 'Humidity', 'Light',
            'Temperature', 'Equipment Fault', 'Plants',
            'Blossoms', 'Fruit', 'Min Height', 'Max Height',
            'Median Height', 'Notes')

        for field in fields:
            self.assertIn(field, records[0].keys())

        # testing boolean conversion
        self.assertFalse(records[0]['Equipment Fault'])

        self.file1_open.assert_called_with('file1', 'r', encoding='utf-8')

    @mock.patch('abq_data_entry.models.os.path.exists')
    def test_get_record(self, mock_exists):
        mock_exists.return_value = True

        with mock.patch(
                'abq_data_entry.models.open',
                self.file1_open
        ):
            record0 = self.model1.get_record(0)
            record1 = self.model1.get_record(1)

        self.assertNotEqual(record0, record1)
        self.assertEqual(record0['Date'], '2018-06-01')
        self.assertEqual(record1['Plot'], '3')
        self.assertEqual(record0['Median Height'], '5.09')

    @mock.patch('abq_data_entry.models.os.path.exists')
    def test_save_record(self, mock_exists):

        record = {
            "Date": '2018-07-01', "Time": '12:00',
            "Technician": 'Test Technician', "Lab": 'E',
            "Plot": '17', "Seed sample": 'test sample',
            "Humidity": '10', "Light": '99',
            "Temperature": '20', "Equipment Fault": False,
            "Plants": '10', "Blossoms": '200',
            "Fruit": '250', "Min Height": '40',
            "Max Height": '50', "Median Height": '55',
            "Notes": 'Test Note\r\nTest Note\r\n'
        }
        record_as_csv = (
            '2018-07-01,12:00,Test Technician,E,17,test sample,10,99,'
            '20,False,10,200,250,40,50,55,"Test Note\r\nTest Note\r\n"'
            '\r\n')

        # test appending a file
        mock_exists.return_value = True

        # test insert
        with mock.patch('abq_data_entry.models.open', self.file2_open):
            self.model2.save_record(record, None)
            self.file2_open.assert_called_with('file2', 'a', encoding='utf-8')
            file2_handle = self.file2_open()
            file2_handle.write.assert_called_with(record_as_csv)

        # test update
        with mock.patch('abq_data_entry.models.open', self.file1_open):
            self.model1.save_record(record, 1)
            self.file1_open.assert_called_with('file1', 'w', encoding='utf-8')
            file1_handle = self.file1_open()
            file1_handle.write.assert_has_calls([
                mock.call(
                    'Date,Time,Technician,Lab,Plot,Seed sample,Humidity,Light,'
                     'Temperature,Equipment Fault,Plants,Blossoms,Fruit,'
                     'Min Height,Max Height,Median Height,Notes\r\n'),
                mock.call('2018-06-01,8:00,J Simms,A,2,AX478,24.47,1.01,21.44,False,'
                     '14,27,1,2.35,9.2,5.09,\r\n'),
                mock.call('2018-07-01,12:00,Test Technician,E,17,test sample,10,99,'
                     '20,False,10,200,250,40,50,55,"Test Note\r\nTest Note\r\n"'
                     '\r\n')])

        # test new file
        mock_exists.return_value = False
        with mock.patch('abq_data_entry.models.open', self.file2_open):
            self.model2.save_record(record, None)
            file2_handle = self.file2_open()
            file2_handle.write.assert_has_calls([
                mock.call('Date,Time,Technician,Lab,Plot,Seed sample,Humidity,Light,'
                     'Temperature,Equipment Fault,Plants,Blossoms,Fruit,'
                     'Min Height,Max Height,Median Height,Notes\r\n'),
                mock.call(record_as_csv)
            ])
            with self.assertRaises(IndexError):
                self.model2.save_record(record, 2)

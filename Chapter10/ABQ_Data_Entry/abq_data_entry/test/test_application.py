from unittest import TestCase
from unittest.mock import patch
from .. import application


class TestApplication(TestCase):
    records = [
        {'Blossoms': '21', 'Date': '2018-06-01',
         'Equipment Fault': 'False', 'Fruit': '3',
         'Humidity': '24.09', 'Lab': 'A',
         'Light': '1.03', 'Max Height': '8.7',
         'Median Height': '2.73', 'Min Height': '1.67',
         'Notes': '\n\n', 'Plants': '9',
         'Plot': '1', 'Seed sample': 'AX477',
         'Technician': 'J Simms', 'Temperature': '22.01',
         'Time': '8:00'
        },
        {'Blossoms': '27', 'Date': '2018-06-01',
         'Equipment Fault': 'False', 'Fruit': '1',
         'Humidity': '24.47', 'Lab': 'A',
         'Light': '1.01', 'Max Height': '9.2',
         'Median Height': '5.09', 'Min Height': '2.35',
         'Notes': '', 'Plants': '14',
         'Plot': '2', 'Seed sample': 'AX478',
         'Technician': 'J Simms', 'Temperature': '21.44',
         'Time': '8:00'}
    ]

    settings = {
                'autofill date': {'type': 'bool', 'value': True},
                'autofill sheet data': {'type': 'bool', 'value': True},
                'font size': {'type': 'int', 'value': 9},
                'theme': {'type': 'str', 'value': 'default'}
            }

    def setUp(self):
        with \
            patch('abq_data_entry.application.m.CSVModel') as csvmodel,\
            patch('abq_data_entry.application.m.SettingsModel') as settingsmodel,\
            patch('abq_data_entry.application.v.DataRecordForm'),\
            patch('abq_data_entry.application.v.RecordList'),\
            patch('abq_data_entry.application.get_main_menu_for_os')\
        :

            settingsmodel().variables = self.settings
            csvmodel().get_all_records.return_value = self.records
            self.app = application.Application()

    def tearDown(self):
        self.app.update()
        self.app.destroy()

    def test_show_recordlist(self):
        self.app.show_recordlist()
        self.app.update()
        self.app.recordlist.tkraise.assert_called()

    def test_populate_recordlist(self):
        # test correct functions
        self.app.populate_recordlist()
        self.app.data_model.get_all_records.assert_called()
        self.app.recordlist.populate.assert_called_with(self.records)

        # test exceptions

        self.app.data_model.get_all_records.side_effect = Exception('Test message')
        with patch('abq_data_entry.application.messagebox'):
            self.app.populate_recordlist()
            application.messagebox.showerror.assert_called_with(
                title='Error', message='Problem reading file',
                detail='Test message'
            )

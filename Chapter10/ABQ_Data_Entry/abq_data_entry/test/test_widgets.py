from .. import widgets
from unittest import TestCase
from unittest.mock import Mock
import tkinter as tk
from tkinter import ttk


class TkTestCase(TestCase):
    """A test case designed for Tkinter widgets and views"""

    keysyms = {
        '-': 'minus',
        ' ': 'space',
        ':': 'colon',
        #  For more see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    }
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.wait_visibility()

    @classmethod
    def tearDownClass(cls):
        cls.root.update()
        cls.root.destroy()

    def type_in_widget(self, widget, string):
        widget.focus_force()
        for char in string:
            char = self.keysyms.get(char, char)
            widget.event_generate('<KeyPress-{}>'.format(char))
            self.root.update()

    def click_on_widget(self, widget, x, y, button=1):
        widget.focus_force()
        self.root.update()
        widget.event_generate("<ButtonPress-{}>".format(button), x=x, y=y)
        self.root.update()


class TestValidatedMixin(TkTestCase):

    def setUp(self):
        class TestClass(widgets.ValidatedMixin, ttk.Entry):
            pass
        self.vw1 = TestClass(self.root)

    def assertEndsWith(self, text, ending):
        if not text.endswith(ending):
            raise AssertionError(
                "'{}' does not end with '{}'".format(text, ending)
            )

    def test_init(self):

        # check error var setup
        self.assertIsInstance(self.vw1.error, tk.StringVar)

        # check validation config
        self.assertEqual(self.vw1.cget('validate'), 'all')
        self.assertEndsWith(
            self.vw1.cget('validatecommand'),
            '%P %s %S %V %i %d'
        )
        self.assertEndsWith(
            self.vw1.cget('invalidcommand'),
            '%P %s %S %V %i %d'
        )

    def test__validate(self):

        # by default, _validate should return true
        args = {
            'proposed': 'abc',
            'current': 'ab',
            'char': 'c',
            'event': 'key',
            'index': '2',
            'action': '1'
        }
        # test key validate routing
        self.assertTrue(
            self.vw1._validate(**args)
        )
        fake_key_val = Mock(return_value=False)
        self.vw1._key_validate = fake_key_val
        self.assertFalse(
            self.vw1._validate(**args)
        )
        fake_key_val.assert_called_with(**args)

        # test focusout validate routing
        args['event'] = 'focusout'
        self.assertTrue(self.vw1._validate(**args))
        fake_focusout_val = Mock(return_value=False)
        self.vw1._focusout_validate = fake_focusout_val
        self.assertFalse(self.vw1._validate(**args))
        fake_focusout_val.assert_called_with(event='focusout')


    def test_trigger_focusout_validation(self):

        fake_focusout_val = Mock(return_value=False)
        self.vw1._focusout_validate = fake_focusout_val
        fake_focusout_invalid = Mock()
        self.vw1._focusout_invalid = fake_focusout_invalid

        val = self.vw1.trigger_focusout_validation()
        self.assertFalse(val)
        fake_focusout_val.assert_called_with(event='focusout')
        fake_focusout_invalid.assert_called_with(event='focusout')


class TestValidatedSpinbox(TkTestCase):

    def setUp(self):
        self.value = tk.DoubleVar()
        self.vsb = widgets.ValidatedSpinbox(
            self.root,
            textvariable=self.value,
            from_=-10, to=10, increment=1
        )
        self.vsb.pack()
        self.vsb.wait_visibility()

    def tearDown(self):
        self.vsb.destroy()

    def key_validate(self, new, current=''):
        return self.vsb._key_validate(
            new,  # inserted char
            'end',  # position to insert
            current,  # current value
            current + new,  # proposed value
            '1'  # action code (1 == insert)
        )

    def click_arrow(self, arrow='inc', times=1):
        x = self.vsb.winfo_width() - 5
        y = 5 if arrow == 'inc' else 15
        for _ in range(times):
            self.click_on_widget(self.vsb, x=x, y=y)

    def test__key_validate(self):
        ###################
        # Unit-test Style #
        ###################

        # test valid input
        for x in range(10):
            x = str(x)
            p_valid = self.vsb._key_validate(x, 'end', '', x, '1')
            n_valid = self.vsb._key_validate(x, 'end', '-', '-' + x, '1')
            self.assertTrue(p_valid)
            self.assertTrue(n_valid)

        # test letters
        valid = self.key_validate('a')
        self.assertFalse(valid)

        # test non-increment number
        valid = self.key_validate('1', '0.')
        self.assertFalse(valid)

        # test too high number
        valid = self.key_validate('0', '10')
        self.assertFalse(valid)

    def test__key_validate_integration(self):
        ##########################
        # Integration test style #
        ##########################

        self.vsb.delete(0, 'end')
        self.type_in_widget(self.vsb, '10')
        self.assertEqual(self.vsb.get(), '10')

        self.vsb.delete(0, 'end')
        self.type_in_widget(self.vsb, 'abcdef')
        self.assertEqual(self.vsb.get(), '')

        self.vsb.delete(0, 'end')
        self.type_in_widget(self.vsb, '200')
        self.assertEqual(self.vsb.get(), '2')

    def test__focusout_validate(self):

        # test valid
        for x in range(10):
            self.value.set(x)
            posvalid = self.vsb._focusout_validate()
            self.value.set(-x)
            negvalid = self.vsb._focusout_validate()

            self.assertTrue(posvalid)
            self.assertTrue(negvalid)

        # test too low
        self.value.set('-200')
        valid = self.vsb._focusout_validate()
        self.assertFalse(valid)

        # test invalid number
        self.vsb.delete(0, 'end')
        self.vsb.insert('end', '-a2-.3')
        valid = self.vsb._focusout_validate()
        self.assertFalse(valid)

    def test_arrows(self):
        self.value.set(0)
        self.click_arrow(times=1)
        self.assertEqual(self.vsb.get(), '1')

        self.click_arrow(times=5)
        self.assertEqual(self.vsb.get(), '6')

        self.click_arrow(arrow='dec', times=1)
        self.assertEqual(self.vsb.get(), '5')

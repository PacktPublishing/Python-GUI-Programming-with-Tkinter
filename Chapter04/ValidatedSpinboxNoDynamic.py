class ValidatedSpinbox(ValidatedMixin, tk.Spinbox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.min = Decimal(str(kwargs.get('from_', '-Infinity')))
        self.max = Decimal(str(kwargs.get('to', 'Infinity')))
        self.resolution = Decimal(str(kwargs.get('increment', '1.0')))
        self.precision = self.resolution.normalize().as_tuple().exponent

    def _key_validate(self, char, index, current, proposed, action, **kwargs):
        valid = True

        no_negative = self.min >= 0
        no_decimal = self.precision >= 0

        if action == '0':
            return True

        # First, filter out obviously invalid keystrokes
        if any([
                (char not in ('-1234567890.')),
                (char == '-' and (no_negative or index != '0')),
                (char == '.' and (no_decimal or '.' in current))
        ]):
            return False

        # At this point, proposed is either '-', '.', '-.',
        # or a valid Decimal string
        if proposed in '-.':
            return True

        # Proposed is a valid Decimal string
        # convert to Decimal and check more:
        proposed = Decimal(proposed)
        proposed_precision = proposed.as_tuple().exponent

        if any([
            (proposed > self.max),
            (proposed_precision < self.precision)
        ]):
            return False

        return valid

    def _focusout_validate(self, **kwargs):

        try:
            value = Decimal(self.get())
        except InvalidOperation:
            self.error.set('Invalid number string')
            return False

        if value < self.min:
            self.error.set('Value is too low (min {})'.format(self.min))
            return False

        return True

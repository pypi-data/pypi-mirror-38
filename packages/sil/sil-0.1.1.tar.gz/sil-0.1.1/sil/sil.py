class Sil:
    '''
    For keeping track of an interative functions status inlineself.


    Class Variables:
        indicator (str): Defaults to '█'. The icon used to print status.
    '''


    indicator='█' #█ █ █ █
    zero_index_q = True

    def __init__(self, total, length=40, every=1):
        '''
        Args:
            total (int): The total number of elements which are being processed.

        Kwargs:
            length (int): The number of characters the progress bar should be.
                Defaults to 40.
            every (int): After how many elements should the progress bar be
                updated. Defaults to 1.

        Returns:
            None
        '''

        self.total = total;
        self.length = length;
        self.current = -1
        self._index = 1
        self.every = every


    def empty(self):
        '''
        Returns:
            (str): an empty status bar
        '''
        blank = ' ' * self.length;
        str = '\r[{}\t{}/{}]'.format(blank, self.current+1, self.total)
        # f'\r[{blank}\t{self.current+1}/{self.total}]'
        return str

    def progress_string(self):
        '''
        Returns:
            (str): the status bar
        '''
        indicators = self.indicator * self.indicators_needed();
        blank = ' ' * (self.length - self.indicators_needed());
        str = '\r[{}{}]\t{}/{}'.format(indicators, blank, self.current+1, self.total)
        # f'\r[{indicators}{blank}]\t{self.current+1}/{self.total}'
        return str

    def fraction_complete(self):
        '''
        Returns:
            (float): (current + 1) / total
        '''
        return (self.current+1) / self.total;

    def indicators_needed(self):
        '''
        Returns:
            (int): round((current + 1) / total * length)
        '''
        return round(self.fraction_complete() * self.length);

    def print_progress(self, prefix='', suffix=''):
        '''
        Prints the status bar.

        Kwargs:
            prefix (str): Defaults to ''. String added prior to status bar.
            suffix (str): Defaults to ''. String added after the status bar.

        Returns:
            None
        '''
        final_q = (self.current+1) == self.total
        if not (final_q or self.check_rate()): return
        self._index = 0
        progress_bar = self.progress_string()
        flush_q = False if final_q else True
        end = '\n' if final_q else ''
        print(prefix+progress_bar+suffix, end=end, flush=flush_q)

    def check_rate(self):
        '''
        Checks to see if the internal index has passed the rate at which to
        print.

        Returns:
            (bool): (self._index > self.every)
        '''
        return self._index > self.every

    def tick(self, prefix='', suffix=''):
        '''
        Increments current and internal index by 1.

        Kwargs:
            prefix (str): Defaults to ''. String added prior to status bar.
            suffix (str): Defaults to ''. String added after the status bar.

        Returns:
            None
        '''
        self.current += 1
        self._index += 1
        self.print_progress()

    def update(self, current=None, prefix='', suffix=''):
        '''
        Kwargs:
            current (int): Defaults to None. The value at which to set the status to.
            prefix (str): Defaults to ''. String added prior to status bar.
            suffix (str): Defaults to ''. String added after the status bar.
        '''
        if current is None:
            self.tick(prefix, suffix)
        else:
            previous = self.current
            self.current = current
            self._index += current - previous
            self.print_progress(prefix, suffix)

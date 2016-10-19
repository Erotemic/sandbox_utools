from __future__ import absolute_import, division, print_function, unicode_literals  # NOQA
import utool as ut
import numpy as np
import pandas as pd
print, rrr, profile = ut.inject2(__name__)


def monkey_to_str_columns(self):
    frame = self.tr_frame
    highlight_func = 'max'
    highlight_func = ut.partial(np.argmax, axis=1)
    highlight_cols = self.highlight_cols

    perrow_colxs = highlight_func(frame[highlight_cols].values)
    n_rows = len(perrow_colxs)
    n_cols = len(highlight_cols)
    shape = (n_rows, n_cols)
    flat_idxs = np.ravel_multi_index((np.arange(n_rows), perrow_colxs), shape)
    flags2d = np.zeros(shape, dtype=np.int32)
    flags2d.ravel()[flat_idxs] = 1
    # np.unravel_index(flat_idxs, shape)

    def color_func(val, level):
        if level:
            return ut.color_text(val, 'red')
        else:
            return val

    _make_fixed_width = pd.formats.format._make_fixed_width
    frame = self.tr_frame
    str_index = self._get_formatted_index(frame)
    str_columns = self._get_formatted_column_labels(frame)
    if self.header:
        stringified = []
        for i, c in enumerate(frame):
            cheader = str_columns[i]
            max_colwidth = max(self.col_space or 0, *(self.adj.len(x)
                                                      for x in cheader))
            fmt_values = self._format_col(i)
            fmt_values = _make_fixed_width(fmt_values, self.justify,
                                           minimum=max_colwidth,
                                           adj=self.adj)
            max_len = max(np.max([self.adj.len(x) for x in fmt_values]),
                          max_colwidth)
            cheader = self.adj.justify(cheader, max_len, mode=self.justify)

            # Apply custom coloring
            # cflags = flags2d.T[i]
            # fmt_values = [color_func(val, level) for val, level in zip(fmt_values, cflags)]

            stringified.append(cheader + fmt_values)
    else:
        stringified = []
        for i, c in enumerate(frame):
            fmt_values = self._format_col(i)
            fmt_values = _make_fixed_width(fmt_values, self.justify,
                                           minimum=(self.col_space or 0),
                                           adj=self.adj)

            stringified.append(fmt_values)

    strcols = stringified
    if self.index:
        strcols.insert(0, str_index)

    # Add ... to signal truncated
    truncate_h = self.truncate_h
    truncate_v = self.truncate_v

    if truncate_h:
        col_num = self.tr_col_num
        # infer from column header
        col_width = self.adj.len(strcols[self.tr_size_col][0])
        strcols.insert(self.tr_col_num + 1, ['...'.center(col_width)] *
                       (len(str_index)))
    if truncate_v:
        n_header_rows = len(str_index) - len(frame)
        row_num = self.tr_row_num
        for ix, col in enumerate(strcols):
            # infer from above row
            cwidth = self.adj.len(strcols[ix][row_num])
            is_dot_col = False
            if truncate_h:
                is_dot_col = ix == col_num + 1
            if cwidth > 3 or is_dot_col:
                my_str = '...'
            else:
                my_str = '..'

            if ix == 0:
                dot_mode = 'left'
            elif is_dot_col:
                cwidth = self.adj.len(strcols[self.tr_size_col][0])
                dot_mode = 'center'
            else:
                dot_mode = 'right'
            dot_str = self.adj.justify([my_str], cwidth, mode=dot_mode)[0]
            strcols[ix].insert(row_num + n_header_rows, dot_str)

    for cx_ in highlight_cols:
        cx = cx_ + bool(self.header)
        col = strcols[cx]
        for rx, val in enumerate(col[1:], start=1):
            strcols[cx][rx] = color_func(val, flags2d[rx - 1, cx - 1])

    return strcols


def to_string_monkey(df, highlight_cols=[0, 1]):
    """  monkey patch to pandas to highlight the maximum value in specified
    cols of a row """
    kwds = dict(buf=None, columns=None, col_space=None, header=True,
                index=True, na_rep='NaN', formatters=None,
                float_format=None, sparsify=None, index_names=True,
                justify=None, line_width=None, max_rows=None,
                max_cols=None, show_dimensions=False)
    self = pd.formats.format.DataFrameFormatter(df, **kwds)
    self.highlight_cols = highlight_cols
    ut.inject_func_as_method(self, monkey_to_str_columns, '_to_str_columns', override=True, force=True)
    def strip_ansi(text):
        import re
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)
    def justify_ansi(self, texts, max_len, mode='right'):
        if mode == 'left':
            return [x.ljust(max_len + (len(x) - len(strip_ansi(x)))) for x in texts]
        elif mode == 'center':
            return [x.center(max_len + (len(x) - len(strip_ansi(x)))) for x in texts]
        else:
            return [x.rjust(max_len + (len(x) - len(strip_ansi(x)))) for x in texts]
    def strlen_ansii(self, text):
        return pd.compat.strlen(strip_ansi(text), encoding=self.encoding)
    ut.inject_func_as_method(self.adj, strlen_ansii, 'len', override=True, force=True)
    ut.inject_func_as_method(self.adj, justify_ansi, 'justify', override=True, force=True)
    # strcols = monkey_to_str_columns(self)
    # texts = strcols[2]
    # str_ = self.adj.adjoin(1, *strcols)
    # print(str_)
    # print(strip_ansi(str_))
    self.to_string()
    result = self.buf.getvalue()
    return result

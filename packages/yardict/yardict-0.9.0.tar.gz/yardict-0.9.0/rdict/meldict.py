from itertools import tee, zip_longest

from .rangedict import RangeDict


class MeldDict(RangeDict):

    def occupy(self, start, end, value, **meld_opts):
        overlapped = list(self.irange(start, end))
        if not overlapped:
            self._occupy(start, end, value)
            return

        if start < overlapped[0].start:
            self._occupy(start, overlapped[0].start, value)

        _end = None
        for reg, next_reg in pairwise(overlapped):

            if next_reg is not None:
                self._occupy(reg.end, next_reg.start, value)

            _end = min(end, reg.end)
            _start = max(start, reg.start)
            if _start < _end:
                self._occupy(_start, _end, self._meld(reg.value, value, **meld_opts))
                continue

            break

        if end > _end:
            self._occupy(_end, end, value)

    def _meld(self, old_val, new_val, **kwargs):  # pylint:disable=unused-argument
        return new_val


def pairwise(iterable, longest=True):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return (zip_longest if longest else zip)(a, b)

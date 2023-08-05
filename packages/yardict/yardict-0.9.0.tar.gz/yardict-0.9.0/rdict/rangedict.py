from io import StringIO
from collections import MutableMapping, deque


class _NOT_GIVEN:
    pass


class RangeItem(object):

    def __init__(self, start, end, value):
        self.start = start
        self.end = end
        self.value = value

    def __eq__(self, other):
        if isinstance(other, RangeItem):
            return self.start == other.start \
                   and self.end == other.end \
                   and self.value == other.value
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, RangeItem):
            return self.start < other.start
        raise TypeError

    def __hash__(self):
        return hash((self.start, self.end, self.value))

    def __repr__(self):
        return '<RangeKey(%s, %s, %s)>' % (self.start, self.end, self.value)

    def __le__(self, other):
        if isinstance(other, RangeItem):
            return self.start < other.start
        raise TypeError

    def copy(self):
        return RangeItem(self.start, self.end, self.value)


class RangeDict(MutableMapping):

    def __init__(self):
        self._list = []

    def __repr__(self):
        _ = ", empty" if not self._list else " with %d items" % len(self._list)
        return "<%s%s>" % (self.__class__.__name__, _)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._item_at(key).value

        elif isinstance(key, slice):
            if key.step is not None:
                raise ValueError(key.step)
            return list(self.islice(key.start, key.stop))

        else:
            raise TypeError(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._occupy(key, key + 1, value)

        elif isinstance(key, slice):
            if key.step is not None:
                raise ValueError(key.step)
            self._occupy(key.start, key.stop, value)

        else:
            raise TypeError(key)

    def __len__(self):
        return len(self._list)

    def __contains__(self, key):
        try:
            _ = self._item_at(key)
        except KeyError:
            return False
        else:
            return True

    def __iter__(self):
        return iter(self._list)

    def __delitem__(self, key):
        if isinstance(key, int):
            self._occupy(key, key + 1, _NOT_GIVEN)

        elif isinstance(key, slice):
            if key.step is not None:
                raise ValueError(key.step)
            self._occupy(key.start, key.stop, _NOT_GIVEN)

        else:
            raise TypeError(key)

    #
    #   ...
    #

    def empty(self):
        return len(self._list) == 0

    def copy(self):
        cls = self.__class__
        copy = cls.__new__(cls)
        copy._list = self._list
        return copy

    def clear(self):
        self._list = []

    def occupy(self, start, end, value):
        self._occupy(start, end, value)

    def get(self, k, default=None):
        try:
            return self._item_at(k).value
        except KeyError:
            return default

    def peek(self, k, default=None):
        try:
            return self._item_at(k)
        except KeyError:
            return default

    def min_key(self):
        return 0 if not self._list else self._list[0].start

    def max_key(self):
        return 0 if not self._list else self._list[-1].end

    def irange(self, start=None, end=None):
        start = self.min_key() if start is None else start
        stop = self.max_key() if end is None else end

        start = self._search(start)
        for item in self._list[start:]:
            if item.start < stop:
                yield item
                continue
            break

    def islice(self, start=None, end=None):
        yield from (item.value for item in self.irange(start, end))

    def dump(self, stream):
        stream.write("%-16s | %-16s | %-8s | %-8s\n" % ('START', 'END', 'SIZE', 'VALUE'))
        stream.write('-' * 79 + '\n')
        for item in self.islice():
            _ = item.start, item.end, item.end - item.start, item.value
            stream.write("%#-16x | %#-16x | %8d | %s\n" % _)

    def dumps(self):
        s = StringIO()
        self.dump(s)
        return s.getvalue()

    #
    #   ...
    #

    @classmethod
    def _make_item(cls, start, end, value):
        return RangeItem(start, end, value)

    def _item_at(self, pos):
        idx = self._search(pos)
        if idx < len(self._list):
            if self._list[idx].start <= pos < self._list[idx].end:
                return self._list[idx]
        raise KeyError(pos)

    def _occupy(self, start, end, value):
        this_item = self._make_item(start, end, value)
        items = deque([this_item])

        left_idx = self._search(this_item.start)
        right_idx = self._search(this_item.end)

        orig_left_idx, left_hanged = left_idx, False
        while 0 <= left_idx < len(self._list):
            left_item = self._list[left_idx]
            if this_item.start < left_item.start:
                left_idx -= 1
                left_hanged = True
                continue
            if self._adjoin_left(this_item, left_item):
                left_item = left_item.copy()
                if self._should_merge(this_item, left_item):
                    self._merge_left(this_item, left_item)
                self._trim_right(left_item, this_item)
                items.appendleft(left_item)
                left_idx -= 1
                left_hanged = left_idx != right_idx
                continue
            elif left_hanged:
                items.appendleft(left_item)
            break

        orig_right_idx, right_hanged = right_idx, False
        while 0 <= right_idx < len(self._list):
            right_item = self._list[right_idx]
            if this_item.end > right_item.end:
                right_idx += 1
                right_hanged = True
                continue
            if self._adjoin_right(this_item, right_item):
                right_item = right_item.copy()
                if self._should_merge(this_item, right_item):
                    self._merge_right(this_item, right_item)
                self._trim_left(right_item, this_item)
                items.append(right_item)
                right_idx += 1
                right_hanged = False
                continue
            elif right_hanged:
                items.append(right_item)
            break

        picked_items = [i for i in items if not (i.value is _NOT_GIVEN or i.start == i.end)]
        self._replace(left_idx, right_idx, picked_items)
        return this_item

    def _replace(self, left_idx, right_idx, items):
        left_idx, right_idx = max(left_idx, 0), min(right_idx, len(self._list))
        self._list[left_idx:right_idx] = items

    def _search(self, pos):
        lo = 0
        hi = len(self._list)

        while lo != hi:
            mid = (lo + hi) // 2

            item = self._list[mid]
            if pos < item.start:
                hi = mid
            elif pos >= item.end:
                lo = mid + 1
            else:
                lo = mid
                break

        return lo

    def _adjoin_left(self, this_item, left_item):
        return left_item.start <= this_item.start <= left_item.end

    def _adjoin_right(self, this_item, right_item):
        return right_item.end >= this_item.end >= right_item.start

    def _should_merge(self, this_item, other_item):
        return this_item.value == other_item.value

    def _trim_left(self, this_item, left_item):
        this_item.start = left_item.end

    def _trim_right(self, this_item, right_item):
        this_item.end = right_item.start

    def _merge_left(self, this_item, left_item):
        this_item.start = left_item.start

    def _merge_right(self, this_item, right_item):
        this_item.end = right_item.end

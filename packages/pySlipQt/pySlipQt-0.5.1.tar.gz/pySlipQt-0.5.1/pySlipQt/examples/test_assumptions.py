#!/usr/bin/env python

"""
Test PySlipQt assumptions.

We make some assumptions in pySlipQt about relative speeds
of various operations.  Make sure those assumptions hold.
"""


import os
import time
import unittest


class TestAssumptions(unittest.TestCase):

    def test_copy_list(self):
        """Check 'l_poly = list(poly)' gets us a new list.

        At a few places in pySlipQt we need a copy of a list, not the original.
        We do this by:
            l_poly = list(poly)
            new_poly = l_poly[:]
        Is the final ...[:] required?
        """

        # try to make copy without [:]
        old_list = [1, 2, 3, 4]
        old_list_id = id(old_list)
        new_list = list(old_list)
        new_list_id = id(new_list)

        # make sure we DO have a copy
        msg = ("'new_list = list(old_list)' DOESN'T give us a copy?\n"
                   "id(old_list)=%d, id(new_list)=%d"
               % (old_list_id, new_list_id))
        self.assertTrue(old_list_id != new_list_id, msg)

    def test_copy(self):
        """Test 'new_list = old_list[:]' does give us a copy.

        At a few places in pySlipQt we need a copy of a list, not the original.
        We do this by:
            new_poly = l_poly[:]
        """

        # try to make a copy with [:]
        old_list = [1, 2, 3, 4]
        old_list_id = id(old_list)
        new_list = old_list[:]
        new_list_id = id(new_list)

        msg = ("'new_list = old_list[:]' DOESN'T give us a copy?\n"
                   "id(old_list)=%d, id(new_list)=%d"
               % (old_list_id, new_list_id))
        self.assertTrue(old_list_id != new_list_id, msg)

    def test_copy2(self):
        """Check 'list(poly)' is faster than 'poly[:]'.

        At a few places in pySlipQt we need a copy of a list and we do:
            new_poly = list(poly)
        Is this faster than:
            new_poly = poly[:]
        """

        loops = 100000

        # create the old list
        old_list = [1, 2, 3, 4, 5, 6]

        # time list() approach
        start = time.time()
        for _ in range(loops):
            new_list = list(old_list)
        list_delta = time.time() - start

        # time copy approach
        start = time.time()
        for _ in range(loops):
            new_list = old_list[:]
        copy_delta = time.time() - start

        msg = ("'old_list[:]' is SLOWER than 'list(old_list)'?\n"
                "old_list[:]=%.1f, list(old_list)=%.1f "
                "(list() is %.2f times faster)"
               % (list_delta, copy_delta,
                   (copy_delta/list_delta)))
        self.assertTrue(list_delta > copy_delta, msg)

    def test_dispatch_slower(self):
        """Test that dispatch is faster than function if/elif/else.

        pySlipQt used to use code like this:
            x = ...
            y = ...
            test = {'ab': 'x+=1;y-=1',
                    'bc': 'x+=2;y+=3',
                    ...
                   }
            exec test['ab']

        Compare the above with something like:
            def test(x, y, place, x_off, y_off):
                if place == 'ab':
                    x += 1
                    y -= 1
                elif place == 'bc':
                    ...

                return (x, y)

            x = ...
            y = ...
            (x, y) = test(x, y, place, x_off, y_off)

        The function approach (which we use) should be faster.
        """

        LOOPS = 1000000

        # check exec timing
        test = {'cc': 'x+=x_off-w2;  y+=y_off-h2',
                'nw': 'x+=x_off;     y+=y_off',
                'cn': 'x+=x_off-w2;  y+=y_off',
                'ne': 'x+=x_off-w;   y+=y_off',
                'ce': 'x+=x_off-w;   y+=y_off-h2',
                'se': 'x+=x_off-w;   y+=y_off-h',
                'cs': 'x+=x_off-w2;  y+=y_off-h',
                'sw': 'x+=x_off;     y+=y_off-h',
                'cw': 'x+=x_off;     y+=y_off-h2',
                None: '',
                False: '',
                '': ''}
        for key in test:
            test[key] = compile(test[key], 'string', 'exec')

        start = time.time()
        for _ in range(LOOPS):
            x = 0
            y = 0
            place = 'nw'
            x_off = 1
            y_off = 3
            w = 100
            w2 = w/2
            h = 100
            h2 = h/2
            exec(test[place])
        exec_delta = time.time() - start

        # now for function equivalent
        def test(x, y, place, w, h, x_off, y_off):
            w2 = w/2
            h2 = h/2
            if place == 'cc':
                x+=x_off-w2;  y+=y_off-h2
            elif place == 'nw':
                x+=x_off;     y+=y_off
            elif place == 'cn':
                x+=x_off-w2;  y+=y_off
            elif place == 'ne':
                x+=x_off-w;   y+=y_off
            elif place == 'ce':
                x+=x_off-w;   y+=y_off-h2
            elif place == 'se':
                x+=x_off-w;   y+=y_off-h
            elif place == 'cs':
                x+=x_off-w2;  y+=y_off-h
            elif place == 'sw':
                x+=x_off;     y+=y_off-h
            elif place == 'cw':
                x+=x_off;     y+=y_off-h2
         
            return (x, y)

        start = time.time()
        for _ in range(LOOPS):
            x = 0
            y = 0
            place = 'nw'
            x_off = 1
            y_off = 3
            w = 100
            h = 100
            (x, y) = test(x, y, place, w, h, x_off, y_off)
        func_delta = time.time() - start

        msg = ("Function if/else is slower than 'exec dispatch[i]'?\n"
                   "exec=%.2fs, function=%.2fs (exec is %.1f times faster)"
               % (exec_delta, func_delta, func_delta/exec_delta))
        self.assertTrue(exec_delta > func_delta, msg)

    def test_copy_faster(self):
        """Test that a[:] copy is slower than copy.deepcopy(a)."""

        import copy

        loops = 100000

        a = [1,2,3,4,5,6,7,8,9,0]   # fake a Z-order list

        start = time.time()
        for _ in range(loops):
            b = copy.deepcopy(a)
        copy_delta = time.time() - start

        start = time.time()
        for _ in range(loops):
            b = a[:]
        clone_delta = time.time() - start

        msg = ('copy.deepcopy() is faster than clone[:]?\n'
                   'copy=%.2fs, clone=%.2fs'
               % (copy_delta, clone_delta))
        self.assertTrue(clone_delta < copy_delta, msg)

    def test_tuple_faster(self):
        """Test unpacking tuple is faster than data object attributes."""

        class DataObj(object):
            def __init__(self, *args, **kwargs):
                if len(args) > 0:
                    msg = 'DataObj() must be called with keyword args ONLY!'
                    raise RuntimeError(msg)

                self.__dict__ = kwargs

        tuple_obj = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        data_obj = DataObj(one=1, two=2, three=3, four=4, five=5,
                           six=6, seven=7, eight=8, nine=9, ten=10)

        loops = 100000

        # time tuple object
        start = time.time()
        for _ in range(loops):
            (one, two, three, four, five, six, seven, eight, nine, ten) = tuple_obj
        tuple_delta = time.time() - start

        # time data object
        start = time.time()
        for _ in range(loops):
            one = data_obj.one
            two = data_obj.two
            three = data_obj.three
            four = data_obj.four
            five = data_obj.five
            six = data_obj.six
            seven = data_obj.seven
            eight = data_obj.eight
            nine = data_obj.nine
            ten = data_obj.ten
        data_delta = time.time() - start

        msg = ('Data object is faster than tuple?\ndata=%.2fs, tuple=%.2fs'
               % (data_delta, tuple_delta))
        self.assertTrue(tuple_delta < data_delta, msg)

################################################################################

if __name__ == '__main__':
    suite = unittest.makeSuite(TestAssumptions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)

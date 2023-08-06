# <AK> converted to unittest

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# from six.moves import range  # <AK> unnecessary
import unittest  # <AK> for jt.jnius additions
import sys                                  # <AK> needed for enhancements
if sys.version_info.major >= 3: long = int  # <AK> needed for enhancements

from jnius import autoclass, java_method, PythonJavaClass, cast
from jnius import java_implementer, JavaException  # <AK> for jt.jnius additions
# from nose.tools import *  # <AK> unnecessary


def setUpModule():
    print('0: declare a TestImplem that implement Collection')


class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        #'java/util/Iterator',
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        self.collection = collection
        self.index = index

    @java_method('()Z')
    def hasNext(self):
        return self.index < len(self.collection.data)  # <AK> fix, was: len(...) - 1

    @java_method('()Ljava/lang/Object;')
    def next(self):
        obj = self.collection.data[self.index]
        self.index += 1
        return obj

    @java_method('()Z')
    def hasPrevious(self):
        return self.index - 1 >= 0  # <AK> fix, was: self.index >= 0

    @java_method('()Ljava/lang/Object;')
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        return obj

    @java_method('()I')
    def previousIndex(self):
        return self.index - 1

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.collection.data[index - 1]

    @java_method('(Ljava/lang/Object;)V')
    def set(self, obj):
        self.collection.data[self.index - 1] = obj


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__(*args)
        self.data = list(args)

    @java_method('()Ljava/util/Iterator;')
    def iterator(self):
        it = TestImplemIterator(self)
        return it

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('()I')
    def size(self):
        return len(self.data)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.data[index]

    @java_method('(ILjava/lang/Object;)Ljava/lang/Object;')
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @java_method('()[Ljava/lang/Object;')
    def toArray(self):
        return self.data

    @java_method('()Ljava/util/ListIterator;')
    def listIterator(self):
        it = TestImplemIterator(self)
        return it

    @java_method('(I)Ljava/util/ListIterator;',
                         name='ListIterator')
    def listIteratorI(self, index):
        it = TestImplemIterator(self, index)
        return it


class TestBadSignature(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    @java_method('(Landroid/bluetooth/BluetoothDevice;IB[])V')
    def bad_signature(self, *args):
        """"""  # <AK> changed due to coverage, was: pass


# <AK> additions for jt.jnius

class TestBadInterface1(PythonJavaClass):
    __javainterfaces__ = ['java/nonexistent/List']


@java_implementer('java/nonexistent/List')
class TestBadInterface2(PythonJavaClass):
    pass


class TestBadJavaContext(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']
    __javacontext__ = "unknown context"


# <AK> makes a module-level code as unittests (ProxyTest)
class ProxyTest(unittest.TestCase):

    def test_proxies(self):

        Short = autoclass('java.lang.Short')
        Float = autoclass('java.lang.Float')

        # <AK> extends tests for different types (not only for ints as in original)
        for coll in (list(map(lambda x: bool(x % 2), range(10))),
                    #list(map(Short, range(10))),
                     list(map(int,   range(10))),
                     list(map(long,  range(10))),
                    #list(map(Float, range(10))),
                     list(map(float, range(10))),
                     list(map(lambda x: chr(ord("A") + x), range(10)))):

            print("1: instantiate the class '{}', with some data of '{}'".format(
                  TestImplem.__name__, type(coll[0])))
            a = TestImplem(*coll)
            print(a)
            print(dir(a))
            # <AK> added
            self.assertEqual(a.hashCode_(), str(a.hashCode()))
            self.assertEqual(a.hashCode_(), str(a.hashCode()))
            self.assertIs(a.equals(a), True)
            self.assertIs(a.equals(TestImplem(*coll)), False)
            self.assertEqual(super(TestImplem, a).toString(), str(a))
            self.assertEqual(a.toString(), str(a))
            # </AK>

            print('2: Tries to get a ListIterator')
            iterator = a.listIterator()
            print('iterator is', iterator)
            #print(iterator.toString())
            self.assertIs(iterator.hasPrevious(), False)
            while iterator.hasNext():
                idx  = iterator.index
                elem = iterator.next()
                print('at index', idx, 'value is', elem)
                # <AK> added
                prev = iterator.previous()
                self.assertEqual(prev, elem)
                self.assertEqual(iterator.next(), elem)
                self.assertEqual(elem, coll[idx])
                self.assertEqual(iterator.get(iterator.index), coll[idx])
                self.assertIs(iterator.hasPrevious(), True)
                self.assertEqual(iterator.previousIndex(), idx)
                # </AK>
            # <AK> added
            iterator = a.listIteratorI(5)
            print('iterator (from index) is', iterator)
            self.assertIs(iterator.hasPrevious(), True)
            while iterator.hasNext():
                idx  = iterator.index
                elem = iterator.next()
                print('at index', idx, 'value is', elem)
                prev = iterator.previous()
                self.assertEqual(prev, elem)
                self.assertEqual(iterator.next(), elem)
                self.assertEqual(elem, coll[idx])
                self.assertEqual(iterator.get(iterator.index), coll[idx])
                self.assertIs(iterator.hasPrevious(), True)
                self.assertEqual(iterator.previousIndex(), idx)
            # </AK>

            print('3: Do cast to a collection')
            a2 = cast('java/util/Collection', a.j_self)
            print(a2)

            print('4: Try few method on the collection')
            Collections = autoclass('java.util.Collections')
            #print(Collections.enumeration(a))

            ret = Collections.max(a)
            print('Collections.max():', ret)
            self.assertEqual(ret, max(coll))  # <AK> added
            # XXX We have issues for methods with multiple signature
            ret = Collections.max(a2)
            self.assertEqual(ret, max(coll))  # <AK> added

            print('Order of data before Collections.reverse():', a.data)
            Collections.reverse(a)
            print('Order of data after  Collections.reverse():', a.data)
            coll = list(reversed(coll))     # <AK> added
            self.assertEqual(a.data, coll)  # <AK> added

            print('Order of data before Collections.swap(2,3):', a.data)
            Collections.swap(a, 2, 3)
            print('Order of data after  Collections.swap(2,3):', a.data)
            coll[2], coll[3] = coll[3], coll[2]  # <AK> added
            self.assertEqual(a.data, coll)       # <AK> added

            print('Order of data before Collections.rotate(5):', a.data)
            Collections.rotate(a, 5)
            print('Order of data after  Collections.rotate(5):', a.data)
            coll = coll[-5:] + coll[:-5]    # <AK> added
            self.assertEqual(a.data, coll)  # <AK> added

            print('Order of data before shuffle():', a.data)
            Collections.shuffle(a)
            print('Order of data after  shuffle():', a.data)

    def test_bad_signature(self):
        # test bad signature
        with self.assertRaises(Exception,  # <AK> changed to use 'with'
                               msg="Failed to throw for bad signature") as exc:
            TestBadSignature()

    # <AK> additions for jt.jnius

    def test_bad_interface(self):
        # test bad interface
        for TestBadInterface in (TestBadInterface1, TestBadInterface2):
            with self.assertRaises(JavaException,
                                   msg="Failed to throw for bad interface") as exc:
                TestBadInterface()

    def test_bad_javacontext(self):
        # test bad __javacontext__
        with self.assertRaises(Exception,
                               msg="Failed to throw for bad __javacontext__") as exc:
            TestBadJavaContext()

    # </AK>

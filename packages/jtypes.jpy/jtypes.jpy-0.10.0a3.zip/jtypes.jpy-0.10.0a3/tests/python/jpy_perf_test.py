import unittest
import time
import random
from jt import jpyutil
jpyutil.init_jvm(jvm_maxmem='512M')
import jpy
from . import with_performance  # <AK> added


class TestPerformance(unittest.TestCase):

    @unittest.skipUnless(True, "performance affected tests turned off")
    def test_general_rt_perf(self):

        Integer = jpy.get_type('java.lang.Integer')
        String = jpy.get_type('java.lang.String')
        File = jpy.get_type('java.io.File')
        HashMap = jpy.get_type('java.util.HashMap')

        # 1 million
        N = 1000000 if with_performance() else 10  # <AK> was: 1000000

        indexes = list(range(N))
        random.shuffle(indexes)

        t0 = time.time()
        pairs = [(Integer(index), File('path')) for index in indexes]
        t1 = time.time()
        print('Integer + File object instantiation took', t1-t0, 's for', N, 'calls, this is', 1000*(t1-t0)/N, 'ms per call')

        map = HashMap()

        t0 = time.time()
        for pair in pairs:
            i, f = pair
            map.put(i, f)
        t1 = time.time()
        print('HashMap.put() took', t1-t0, 's for', N, 'calls, this is', 1000*(t1-t0)/N, 'ms per call')

        t0 = time.time()
        for pair in pairs:
            i, f = pair
            f = map.get(i)
        t1 = time.time()
        print('HashMap.get() took', t1-t0, 's for', N, 'calls, this is', 1000*(t1-t0)/N, 'ms per call')



if __name__ == '__main__':
    print('\nRunning ' + __file__)
    unittest.main()

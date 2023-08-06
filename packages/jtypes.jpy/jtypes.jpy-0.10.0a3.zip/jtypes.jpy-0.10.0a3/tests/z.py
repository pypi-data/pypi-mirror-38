import os

import jt.jpyutil as jpyutil

testd = os.path.dirname(os.path.abspath(__file__))
jpyutil.init_jvm(jvm_maxmem='512M', jvm_classpath=[os.path.join(testd,"java","classes")])
import jt.jpy as jpy

Fixture = jpy.get_type('org.jpy.fixtures.FieldTestFixture')

assert Fixture.z_STATIC_FIELD == True
assert Fixture.c_STATIC_FIELD == 65
assert Fixture.b_STATIC_FIELD == 123
assert Fixture.s_STATIC_FIELD == 12345
assert Fixture.i_STATIC_FIELD == 123456789
assert Fixture.j_STATIC_FIELD == 1234567890123456789

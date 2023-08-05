from tests.example import Example


inst1 = Example()
inst2 = Example()
inst3 = Example()
inst1.print_count()
inst2.print_count()
inst3.print_count()
assert inst1 == inst2
assert inst2 == inst3
assert inst1 is inst2
assert Example.count == 1

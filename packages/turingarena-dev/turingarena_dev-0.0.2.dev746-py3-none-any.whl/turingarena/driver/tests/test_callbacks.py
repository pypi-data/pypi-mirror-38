from collections import deque

from turingarena.driver.tests.test_utils import define_algorithms


def callback_mock(calls, return_values=None):
    if return_values is not None:
        return_values = deque(return_values)

    def mock(*args):
        calls.append((mock, args))

        if return_values is not None:
            return return_values.popleft()

    return mock


def test_callback_no_arguments():
    for algo in define_algorithms(
            interface_text="""
                procedure test() callbacks {
                    procedure c();
                }
                
                main {
                    call test() callbacks {
                        procedure c() {}
                    }
                }
            """,
            sources={
                'C++': """
                    void test(void c()) {
                        c();
                        c();
                    }
                """,
                'Python': """if True:                    
                    def test(c):
                        c()
                        c()
                """,
            }
    ):
        with algo.run() as p:
            calls = []
            c = callback_mock(calls)
            p.procedures.test(callbacks=[lambda: c()])

            assert calls == [
                (c, ()),
                (c, ()),
            ]


def test_callback_with_arguments():
    for algo in define_algorithms(
            interface_text="""
                procedure test() callbacks {
                    procedure c(a, b);
                }
                
                main {
                    call test() callbacks {
                        procedure c(a, b) {
                            write a, b;
                        }
                    }
                }
            """,
            sources={
                'C++': """
                    void test(void c(int a, int b)) {
                        c(1, 2);
                        c(3, 4);
                    }
                """,
                'Python': """if True:
                    def test(c):
                        c(1, 2)
                        c(3, 4)
                """,
            },
    ):
        with algo.run() as p:
            calls = []
            c = callback_mock(calls)
            p.procedures.test(callbacks=[lambda a, b: c(a, b)])

            assert calls == [
                (c, (1, 2)),
                (c, (3, 4)),
            ]


def test_callback_return_value():
    for algo in define_algorithms(
            interface_text="""
                procedure test() callbacks {
                    function c(a);
                }
                main {
                    call test() callbacks {
                        function c(a) {
                            write a;
                            read b;
                            return b;
                        }
                    }
                    checkpoint;
                }
            """,
            sources={
                'C++': """
                    #include <cassert>
                    void test(int c(int a)) {
                        assert(c(1) == 2);
                        assert(c(3) == 4);
                    }
                """,
                'Python': """if True:
                    def test(c):
                        assert c(1) == 2
                        assert c(3) == 4
                """
            }
    ):
        with algo.run() as p:
            calls = []
            c = callback_mock(calls, [2, 4])
            p.procedures.test(callbacks=[lambda a: c(a)])

            assert calls == [
                (c, (1,)),
                (c, (3,)),
            ]


def test_interface_no_callbacks():
    for algo in define_algorithms(
            interface_text="""
                function test();
                main {
                    call o = test();
                    write o;
                }
            """,
            sources={
                'C++': """
                    int test() {
                        return 1;
                    }
                """,
                'Python': """if True:
                    def test():
                        return 1
                """,
            },
    ):
        with algo.run() as p:
            assert p.functions.test() == 1


def test_interface_one_callback():
    for algo in define_algorithms(
            interface_text="""
                function test() callbacks {
                    procedure cb();
                }
                main {
                    call o = test() callbacks {
                        procedure cb() {}
                    }
                    write o;
                }
            """,
            sources={
                'C++': """
                    int test(void cb()) {
                        cb();
                        cb();
                        return 1;
                    }
                """,
                'Python': """if True:
                    def test(cb):
                        cb()
                        cb()
                        return 1
                """,
            }
    ):
        with algo.run() as p:
            calls = []
            cb = callback_mock(calls)
            assert p.functions.test(callbacks=[cb]) == 1
            assert calls == [
                (cb, ()),
                (cb, ()),
            ]


def test_interface_multiple_callbacks():
    for algo in define_algorithms(
            interface_text="""
                function test() callbacks {
                    procedure cb1();
                    procedure cb2();
                }
                    
                main {
                    call o = test() callbacks {
                        procedure cb1() {}
                        procedure cb2() {}
                    }
                    write o;
                }
            """,
            sources={
                'C++': """
                    int test(void cb1(), void cb2()) {
                        cb1();
                        cb2();
                        cb2();
                        cb1();
                        return 1;
                    }
                """,
                'Python': """if True:
                    def test(cb1, cb2):
                        cb1()
                        cb2()
                        cb2()
                        cb1()
                        return 1
                """,
            },
    ):
        with algo.run() as p:
            calls = []
            cb1 = callback_mock(calls)
            cb2 = callback_mock(calls)
            assert p.functions.test(callbacks=[cb1, cb2]) == 1
            assert calls == [
                (cb1, ()),
                (cb2, ()),
                (cb2, ()),
                (cb1, ()),
            ]

from app.f import hello, world


def test_f():
    assert hello() == "Hello"
    assert world() == "World"
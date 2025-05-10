from typing import Callable


class TestFunction:
    name:str
    function:Callable[[], None]
    def __init__(self, name, func):
        self.name = name
        self.function = func

    def test(self) -> bool:
        try:
            self.function()
        except Exception as e:
            print(f"Exception occured in {e}")
            print(e)
            return False
        return True


test_functions:list[TestFunction] = list()

def testCase(test_name:str):
    global test_functions
    def decorator(func):
        test_functions.append(TestFunction(test_name, func))
    return decorator


def testAll():
    test_count = len(test_functions)
    success_count = 0
    for func in test_functions:
        result = func.test()
        if result:
            success_count += 1
    print(f"{test_count}개 중 {success_count}개 통과했습니다.")

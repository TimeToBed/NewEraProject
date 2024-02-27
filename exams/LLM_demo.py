from LLM_package import *


async def main():
    #可以直接将这两行代码放入指定位置，进行流式异步传输
    async for content in analysis_problem(p_test_problem):
        print(content, end="")

if __name__ == '__main__':
    print(p_test_problem)
    #直接通过函数形式调用
    asyncio.run(main())

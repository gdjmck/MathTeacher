"""
Math Tutor 命令行演示程序

演示三种解题模式的使用
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import MathSolver, MathProblem, SolverMode
from core.llm_client import OpenAIClient


def load_env_file(env_path: str) -> None:
    """加载项目根目录下的 .env 文件"""
    if not os.path.exists(env_path):
        return

    with open(env_path, 'r', encoding='utf-8') as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key and key not in os.environ:
                os.environ[key] = value


load_env_file(os.path.join(os.path.dirname(__file__), '.env'))


def print_header():
    """打印程序头部"""
    print("\n" + "=" * 70)
    print(" " * 20 + "Math Tutor - 数学解题助手")
    print("=" * 70)
    print("\n欢迎使用 Math Tutor！")
    print("当前使用 OpenAI LLM 响应。")
    print("\n可用的解题模式：")
    print("  1. 思路提示 (hint)    - 给出解题方向，引导思考")
    print("  2. 简略思路 (brief)   - 提供完整但简洁的步骤")
    print("  3. 详细详解 (detailed) - 详细讲解每个步骤和知识点")
    print("-" * 70)


def get_user_input():
    """获取用户输入"""
    print("\n请输入数学问题（输入 'quit' 退出）：")
    question = input("> ").strip()

    if question.lower() in ['quit', 'exit', 'q']:
        return None, None

    if not question:
        print("⚠️  题目不能为空！")
        return get_user_input()

    print("\n请选择解题模式（1/2/3）：")
    print("  1 - 思路提示")
    print("  2 - 简略思路")
    print("  3 - 详细详解")

    mode_input = input("> ").strip()

    mode_map = {
        '1': SolverMode.HINT,
        '2': SolverMode.BRIEF,
        '3': SolverMode.DETAILED,
        'hint': SolverMode.HINT,
        'brief': SolverMode.BRIEF,
        'detailed': SolverMode.DETAILED
    }

    mode = mode_map.get(mode_input.lower())

    if mode is None:
        print("⚠️  无效的模式选择，使用默认模式：简略思路")
        mode = SolverMode.BRIEF

    return question, mode


def display_solution(response):
    """展示解题结果"""
    mode_names = {
        SolverMode.HINT: "思路提示",
        SolverMode.BRIEF: "简略思路",
        SolverMode.DETAILED: "详细详解"
    }

    print("\n" + "=" * 70)
    print(f"【题目】{response.problem.question}")
    print(f"【模式】{mode_names[response.mode]}")
    print("-" * 70)
    print(response.content)
    print("=" * 70)

    if response.needs_visualization:
        print("\n💡 提示：此题目可能需要图形辅助理解（可视化功能开发中...）")


def create_solver() -> MathSolver:
    """创建使用 OpenAI 的解题器"""
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError('未配置 OPENAI_API_KEY，无法启动 OpenAI 演示')

    model = os.getenv('LLM_MODEL', 'gpt-4')
    openai_client = OpenAIClient(model=model)
    return MathSolver(llm_client=openai_client)


def run_demo():
    """运行演示程序"""
    print_header()

    solver = create_solver()

    while True:
        question, mode = get_user_input()

        if question is None:
            print("\n感谢使用 Math Tutor！再见！👋")
            break

        # 创建问题对象
        problem = MathProblem(question=question)

        # 解题
        try:
            response = solver.solve(problem, mode)
            display_solution(response)
        except Exception as e:
            print(f"\n❌ 解题出错：{e}")

        print("\n" + "-" * 70)
        print("继续输入新问题，或输入 'quit' 退出")


def run_example():
    """运行预设示例"""
    print_header()
    print("\n运行预设示例...")

    solver = create_solver()

    # 示例问题
    examples = [
        ("求解方程：3x - 7 = 11", SolverMode.HINT),
        ("计算：sin²θ + cos²θ", SolverMode.BRIEF),
        ("证明：√2是无理数", SolverMode.DETAILED),
    ]

    for idx, (question, mode) in enumerate(examples, 1):
        print(f"\n\n{'=' * 70}")
        print(f"示例 {idx}/{len(examples)}")
        print('=' * 70)

        problem = MathProblem(question=question)
        response = solver.solve(problem, mode)
        display_solution(response)

        if idx < len(examples):
            input("\n按Enter继续下一个示例...")

    print("\n\n" + "=" * 70)
    print("所有示例演示完毕！")
    print("=" * 70)


def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        run_example()
    else:
        run_demo()


if __name__ == "__main__":
    main()

import ast
import operator


def safe_calculator(expression):
    """
    安全计算器。
    只允许计算数字和 + - * / ** ()，避免执行危险代码。
    """

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("只允许数字")

        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)

            if op_type not in allowed_operators:
                raise ValueError("不支持这个运算符")

            return allowed_operators[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)

            if op_type not in allowed_operators:
                raise ValueError("不支持这个一元运算符")

            return allowed_operators[op_type](operand)

        raise ValueError("表达式不安全")

    tree = ast.parse(expression, mode="eval")
    return eval_node(tree.body)
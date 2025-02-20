from gooey import Gooey, GooeyParser


@Gooey(
    program_name="富文本打印器",
    program_description="输入并打印富文本内容",
    default_size=(600, 400),
)
def main():
    parser = GooeyParser()

    # 添加多行文本框组件
    parser.add_argument(
        'content',
        metavar='输入内容',
        widget='Textarea',  # 使用多行文本框
        help='在此输入您要打印的内容',
        gooey_options={
            'height': 300,  # 设置文本框高度
            'placeholder': "请输入您的文本内容..."
        }
    )

    args = parser.parse_args()

    # 打印带格式的输出（使用ANSI转义码实现颜色）
    print("\n\033[1;36m=== 打印结果 ===\033[0m")  # 青色标题
    print("\033[1;33m" + args.content + "\033[0m")  # 黄色文本
    print("\033[1;32m✓ 内容已成功打印！\033[0m\n")  # 绿色成功提示


if __name__ == '__main__':
    main()
from DataGnerator import *
def main():
    parser = argparse.ArgumentParser(description='数据生成工具')
    parser.add_argument('--config', type=str, default='config.json', help='配置文件路径')
    parser.add_argument('--output', type=str, default='output.csv', help='输出文件路径')
    parser.add_argument('--num', type=int, default=100, help='生成数据行数')
    args = parser.parse_args()

    # 读取配置文件
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        # 使用默认配置
        config = {
            "fields": [
                {"name": "用户ID", "type": "id"},
                {"name": "姓名", "type": "name"},
                {"name": "年龄", "type": "age", "params": {"min_age": 18, "max_age": 60}},
                {"name": "性别", "type": "choice","params": {"options": ["男", "女"]}},
                {"name": "电话", "type": "phone"},
                {"name": "邮箱", "type": "email"},
                {"name": "地址", "type": "address"},
                {"name": "注册日期", "type": "date", "params": {"start_date": "-365d", "end_date": "today"}},
                {"name": "消费金额", "type": "amount", "params": {"min_val": 0, "max_val": 10000}},
                {"name": "测试", "type": "choice", "params": {"options": ["a", "b", "c"]}},
                {"name": "身份证号", "type": "ssn"},

            ]
        }

    # 生成数据
    generator = DataGenerator()
    data = generator.generate_data(config['fields'], args.num)

    # 生成csv文件
    # output_file = args.output
    # 生成json文件
    output_file = args.config
    if output_file.endswith('.csv'):
        generator.save_to_csv(data, output_file)
    elif output_file.endswith('.json'):
        generator.save_to_json(data, output_file)
    elif output_file.endswith('.xlsx'):
        generator.save_to_excel(data, output_file)
    else:
        print("不支持的文件格式，默认保存为CSV")
        generator.save_to_csv(data, output_file + '.csv')


if __name__ == "__main__":
    main()
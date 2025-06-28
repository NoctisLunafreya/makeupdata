import random
import csv
import json
import argparse
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd


class DataGenerator:
    def __init__(self, seed=42):
        """初始化数据生成器"""
        self.fake = Faker('zh_CN')
        Faker.seed(seed)
        random.seed(seed)

        self.counter = 0  # 初始化计数器
        self.prefix = "USER-"

        # 定义支持的字段类型及其生成函数
        self.field_generators = {
            'id': self.generate_id,
            'name': self.generate_name,
            'age': self.generate_age,
            'gender': self.generate_gender,
            'phone': self.generate_phone,
            'email': self.generate_email,
            'address': self.generate_address,
            'date': self.generate_date,
            'datetime': self.generate_datetime,
            'amount': self.generate_amount,
            'status': self.generate_status,
            'random_str': self.generate_random_str,
            'choice': self.generate_choice,
        }

    def generate_id(self):
        """生成唯一ID"""
        self.counter += 1
        return f"{self.counter:05d}"  # 返回格式如 "USER-00001"

    def generate_name(self):
        """生成姓名"""
        return self.fake.name()

    def generate_age(self, min_age=18, max_age=60):
        """生成年龄"""
        return random.randint(min_age, max_age)

    def generate_gender(self):
        """生成性别"""
        return random.choice(['男', '女'])

    def generate_phone(self):
        """生成手机号"""
        return self.fake.phone_number()

    def generate_email(self):
        """生成邮箱"""
        return self.fake.email()

    def generate_address(self):
        """生成地址"""
        return self.fake.address().replace('\n', ' ')

    def generate_date(self, start_date='-365d', end_date='today'):
        """生成日期"""
        return self.fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

    def generate_datetime(self, start_date='-30d', end_date='now'):
        """生成日期时间"""
        return self.fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M:%S')

    def generate_amount(self, min_val=0, max_val=10000, precision=2):
        """生成金额"""
        return round(random.uniform(min_val, max_val), precision)

    def generate_status(self, options=['正常', '异常', '已处理', '待处理']):
        """生成状态"""
        return random.choice(options)

    def generate_choice(self, options):
        """从给定选项中随机选择一个"""
        return random.choice(options)


    def generate_random_str(self, length=10):
        """生成随机字符串"""
        return self.fake.pystr(min_chars=length, max_chars=length)

    def generate_row(self, fields):
        """根据字段配置生成一行数据"""
        row = {}
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            params = field.get('params', {})

            if field_type in self.field_generators:
                row[field_name] = self.field_generators[field_type](**params)
            else:
                # 未知类型字段，生成随机字符串
                row[field_name] = self.generate_random_str()
        return row

    def generate_data(self, fields, num_rows):
        """生成指定行数的数据"""
        return [self.generate_row(fields) for _ in range(num_rows)]

    def save_to_csv(self, data, filename):
        """保存数据到CSV文件"""
        if not data:
            print("没有数据可保存")
            return

        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"数据已保存到 {filename}")

    def save_to_json(self, data, filename):
        """保存数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filename}")

    def save_to_excel(self, data, filename):
        """保存数据到Excel文件"""
        if not data:
            print("没有数据可保存")
            return

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"数据已保存到 {filename}")


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
                {"name": "性别", "type": "gender"},
                {"name": "电话", "type": "phone"},
                {"name": "邮箱", "type": "email"},
                {"name": "地址", "type": "address"},
                {"name": "注册日期", "type": "date", "params": {"start_date": "-365d", "end_date": "today"}},
                {"name": "消费金额", "type": "amount", "params": {"min_val": 0, "max_val": 10000}},
                {"name": "用户状态", "type": "status", "params": {"options": ["活跃", "休眠", "已注销"]}},
                {"name": "测试", "type": "choice", "params": {"options": ["a", "b", "c"]}}

            ]
        }

    # 生成数据
    generator = DataGenerator()
    data = generator.generate_data(config['fields'], args.num)

    # 保存数据
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
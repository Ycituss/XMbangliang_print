import pandas as pd
import json
import sys


def excel_to_plugin_json(excel_path, output_path='pdddata.json'):
    """
    将 Excel 转换为插件可用的 JSON 格式
    Excel 要求：A列 = ID，B列 = 要加的内容
    """
    try:
        # 读取 Excel，第一行作为表头
        df = pd.read_excel(excel_path, header=0)

        # 检查列数
        if df.shape[1] < 2:
            print("错误：Excel 至少需要两列（A列ID，B列内容）")
            return False

        # 提取 A列和 B列，转换为插件需要的格式
        pdddata = []
        for _, row in df.iterrows():
            id_value = str(row.iloc[0]).strip()
            content_value = str(row.iloc[1]).strip()

            # 跳过空行
            if id_value and content_value:
                pdddata.append([id_value, content_value])

        # 保存为 JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pdddata, f, ensure_ascii=False, indent=2)

        print(f"转换成功！")
        print(f"输出文件：{output_path}")
        print(f"共转换 {len(pdddata)} 条数据")
        print("\n数据预览（前3条）：")
        for i, item in enumerate(pdddata[:3]):
            print(f"  {i + 1}. {item[0]} -> {item[1][:50]}...")

        return True

    except Exception as e:
        print(f"转换失败：{e}")
        return False


# 命令行使用
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python excel_to_json.py <excel文件路径> [输出json路径]")
        print("示例：python excel_to_json.py data.xlsx pdddata.json")
    else:
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'pdddata.json'
        excel_to_plugin_json(excel_file, output_file)
import re
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_reference(line):
    # 定义正则表达式模式
    pattern = re.compile(r'\[(\d+)\]\s+(.*?)\s+“(.*?)”\s+(.*?),\s*(?:vol\.\s*(\d+),\s*)?(?:no\.\s*(\d+),\s*)?(\d{4}),\s*pp\. (\d+)\s*–\s*(\d+)\.')

    match = pattern.match(line)
    if not match:
        logging.warning(f"Line does not match expected format: {line}")
        return None

    # 提取匹配的组
    index, authors, title, journal_or_conference, volume, number, year, pages_start, pages_end = match.groups()

    # 格式化作者列表
    authors = authors.replace(' and ', ', ')

    # 格式化页面范围
    pages = f"{pages_start}--{pages_end}"

    # 判断是期刊文章还是会议论文
    if journal_or_conference.lower() in ["tpami", "ijcv", "tmm", "tip", "tcsvt", "ijcai", "aaai", "iccv", "cvpr",
                                         "eccv", "wacv", "icpr", "icdar", "icml", "nips", "iclr", "icassp", "icra",
                                         "iros", "iccvw", "cvprw", "eccvw", "wacvw", "icprw", "icdarw", "icmlw", "nips",
                                         "iclrw", "icasspw", "icraw", "irosw", "iccvw", "cvprw", "eccvw", "wacvw",
                                         "icprw", "icdarw", "icmlw", "nips", "iclrw", "icasspw", "icraw", "irosw"]:
        bibtex_type = "@inproceedings"
    else:
        bibtex_type = "@article"

    # 生成BibTeX条目
    bibtex_entry = f"""{bibtex_type}{{{authors.lower().replace(' ', '_')}{year}{index},
  title={{{title}}},
  author={{{authors}}},
  journal={{{journal_or_conference}}},
  pages={{{pages}}},
  year={{{year}}},
}}"""

    return bibtex_entry


def convert_to_bibtex(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if line:
                bibtex_entry = parse_reference(line)
                if bibtex_entry:
                    outfile.write(bibtex_entry + "\n\n")
                else:
                    logging.warning(f"No BibTeX entry generated for line: {line}")


# 使用示例
input_file = 'references.txt'  # 输入文件名
output_file = 'references.bib'  # 输出文件名
convert_to_bibtex(input_file, output_file)
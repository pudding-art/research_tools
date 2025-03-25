import re


def parse_reference_to_bibtex(reference):
    # 定义正则表达式来提取关键信息
    pattern = re.compile(
        r'\[(\d+)\]\s+'  # 编号
        r'(?P<authors>[^,]+),\s+'  # 作者
        r'"(?P<title>[^"]+)",\s+'  # 标题
        r'(?P<journal>[^,]+),\s+'  # 期刊
        r'(vol\. (?P<volume>\d+),\s+no\. (?P<number>\d+),\s+)?'  # 卷号和期号（可选）
        r'pp\. (?P<pages>[^,]+),\s+'  # 页码
        r'(?P<year>\d{4})\.'  # 年份
    )

    match = pattern.match(reference)
    if not match:
        raise ValueError("Reference format not recognized")

    # 提取匹配到的字段
    authors = match.group('authors')
    title = match.group('title')
    journal = match.group('journal')
    volume = match.group('volume')
    number = match.group('number')
    pages = match.group('pages')
    year = match.group('year')

    # 处理作者列表，将其转换为 BibTeX 格式
    authors = ' and '.join([author.strip() for author in authors.split(',')])

    # 构造 BibTeX 条目
    bibtex_entry = f"@article{{{authors.replace(' ', '')}{year},\n"
    bibtex_entry += f"  author = {{{authors}}},\n"
    bibtex_entry += f"  title = {{{title}}},\n"
    bibtex_entry += f"  journal = {{{journal}}},\n"
    if volume:
        bibtex_entry += f"  volume = {{{volume}}},\n"
    if number:
        bibtex_entry += f"  number = {{{number}}},\n"
    bibtex_entry += f"  pages = {{{pages}}},\n"
    bibtex_entry += f"  year = {{{year}}}\n"
    bibtex_entry += "}"

    return bibtex_entry


# 示例文献列表
references = [
    "[156] Q. Wang, J. Gao, W. Lin, and X. Li, \"Nwpu-crowd: A large-scale benchmark for crowd counting and localization,\" TPAMI, vol. 43, no. 6, pp. 2141–2149, 2021.",
    "[157] Y. Pang, J. Cao, Y. Li, J. Xie, H. Sun, and J. Gong, \"Tju-dhd: A diverse high-resolution dataset for object detection,\" TIP, vol. 30, pp. 207–219, 2021.",
    "[158] J. Han et al., \"Soda10m: A large-scale 2d self/semi-supervised object detection dataset for autonomous driving,\" arXiv preprint arXiv:2106.11118, 2021.",
    "[159] M.-R. Hsieh, Y.-L. Lin, and W. H. Hsu, \"Drone-based object counting by spatially regularized regional proposal network,\" in ICCV, 2017, pp. 4165–4173.",
    "[160] Z. Cai and N. Vasconcelos, \"Cascade r-cnn: High quality object detection and instance segmentation,\" TPAMI, vol. 43, no. 5, pp. 1483–1498, 2021."
]

# 转换为 BibTeX 并打印
for ref in references:
    try:
        bibtex = parse_reference_to_bibtex(ref)
        print(bibtex)
        print("\n")
    except ValueError as e:
        print(f"Error parsing reference: {e}")
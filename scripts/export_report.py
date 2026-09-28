"""Export the existing analysis for public Pages without machine-specific paths."""
from pathlib import Path
import argparse
import json
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('report', type=Path)
parser.add_argument('evidence', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
site = root / 'site'
site.mkdir(exist_ok=True)
text = args.report.read_text(encoding='utf-8')
text = re.sub(r'<p>实体文件：<code>.*?</code></p>',
              '<p>存储：resources/app.asar.unpacked 下的对应相对路径。</p>', text)
text = text.replace('使用同目录只读检查器查看。', '需在相应版本的本地安装包中复查。')
text = text.replace('完整机器可读定位在同目录 <code>mechanism-evidence.json</code>，只读检查器为 <code>inspect_installation.py</code>。',
    '完整机器可读定位见 <a href="./mechanism-evidence.json">证据索引 JSON</a>；公开页不包含供应商原始代码或安装文件。')
text = text.replace('本地单文件 · 无外部资源依赖', '独立静态报告 · 无外部资源依赖')
text = text.replace('报告独立于 Workflow Foundry 项目；不修改安装程序或用户运行数据。',
    '独立学习分析，非腾讯官方文档。<a href="https://github.com/jiuchenm/workbuddy-study">报告仓库</a>')
assert not re.search(r'[A-Za-z]:[\\/](?:Users|Program Files)|file://', text, re.I), 'Local path remains in public HTML'
records = json.loads(args.evidence.read_text(encoding='utf-8'))
public = [{k: v for k, v in item.items() if k != 'local_path'} for item in records]
(site / 'index.html').write_text(text, encoding='utf-8')
(site / 'mechanism-evidence.json').write_text(json.dumps(public, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(site / '.nojekyll').touch()
print(f'Exported report and {len(public)} evidence records to site/')

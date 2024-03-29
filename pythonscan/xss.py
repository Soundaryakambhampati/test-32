# import os
# import re
# import json
# def read_html_files(path):
   
#     html_files = []
#     for filename in os.listdir(path):
#         if filename.endswith(".html"):
#             file_path = os.path.join(path, filename)
#             with open(file_path, "r", encoding="utf-8") as file:
#                 file_content = file.read()
#                 html_files.append(file_content)
#     return html_files

# def check_xss_vulnerability_in_directory(html_files):
    
#     xss_vulnerabilities = []
#     for file_content in html_files:
#         matches = re.findall("<[^\s<>]*[^\s<>]*(?:\s\w+=(?:(?:\"[^\"]*\")|(?:\'[^\']*\')|[^\"\'>\s]*))*[^\s<>]*\s*(?:(?:\/>)|(?:>[\s\S]*?<\/[^\s<>]*\s*>))|[\s\S]*?(?:(?<=\=)[\'\"]\+[^\"\'>]*?(\+|%2[Bb]){2}[^\S]*?\w*\([^\S]*?[\'\"]\)|(?<=\=)[\'\"][^\"\'>]*?javascript:[^\"\'>]*?((?:(?:\%25)|%)[\dA-Fa-f]{2}){2}[\S]*?)([\"\'][^\"\'>]*?)(?:javascript:\S*?)?['\"]", file_content)
#         if matches:
#             xss_vulnerabilities.append({'matches':matches})
#     return json.dumps(xss_vulnerabilities)
import os
import re
import json


def read_html_files(path):
    html_files = []
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            file_path = os.path.join(path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
                html_files.append(file_content)
    return html_files


def check_xss_vulnerability_in_directory(html_files):
    xss_vulnerabilities = []
    for file_index, file_content in enumerate(html_files, start=1):
        matches = re.findall(r"<[^\s<>]*[^\s<>]*(?:\s\w+=(?:(?:\"[^\"]*\")|(?:\'[^\']*\')|[^\"\'>\s]*))*[^\s<>]*\s*(?:(?:\/>)|(?:>[\s\S]*?<\/[^\s<>]*\s*>))|[\s\S]*?(?:(?<=\=)[\'\"]\+[^\"\'>]*?(\+|%2[Bb]){2}[^\S]*?\w*\([^\S]*?[\'\"]\)|(?<=\=)[\'\"][^\"\'>]*?javascript:[^\"\'>]*?((?:(?:\%25)|%)[\dA-Fa-f]{2}){2}[\S]*?)([\"\'][^\"\'>]*?)(?:javascript:\S*?)?['\"]", file_content)
        if matches:
            lines = file_content.split('\n')
            for i, line in enumerate(lines, start=1):
                for match in matches:
                    if match[1] in line:
                        vulnerability = {
                            'file_index': file_index,
                            'line_number': i,
                            'line_content': line.strip(),
                            'severity': 'medium'
                        }
                        xss_vulnerabilities.append(vulnerability)
    return json.dumps(xss_vulnerabilities, indent=2)
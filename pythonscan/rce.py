import os
import re
import json

def scan_file(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    result = {}

    if re.search(r'request\.(POST|GET)\.(get|post)', contents):
        if re.search(r'eval\(|exec\(|pickle.loads\(|unsafe_load\(|yaml.load\(|paramiko.exec_command\(|SSHClient.invoke_shell\(|shell=True\(', contents):
            result['status'] = 'Vulnerable'
            rce_vuln_lines = []
            lines = contents.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'eval\(|unsafe_load\(|exec\(|pickle.loads\(|yaml.load\(|paramiko.exec_command\(|SSHClient.invoke_shell\(|shell=True\(', line):
                    rce_vuln_lines.append({'line_number': i+1, 'code': line})
            if rce_vuln_lines:
                result['vulnerable_lines'] = rce_vuln_lines
        else:
            print("ok")
    else:
        if re.search(r'eval\(|exec\(|pickle.loads\(|yaml.load\(|unsafe_load\(|paramiko.exec_command\(|SSHClient.invoke_shell\(|shell=True\(', contents):
            result['status'] = 'Potential RCE vulnerability found'
            rce_vuln_lines = []
            lines = contents.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'eval\(|exec\(|pickle.loads\(|yaml.load\(|unsafe_load\(|paramiko.exec_command\(|SSHClient.invoke_shell\(|shell=True\(', line):
                    rce_vuln_lines.append({'line_number': i+1, 'code': line})
            if rce_vuln_lines:
                result['vulnerable_lines'] = rce_vuln_lines
        else:
            print("ok")

    result['file_path'] = file_path

    return result

def scan_directory_rce(path):
    results = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                result = scan_file(full_path)
                results.append(result)

    output = json.dumps(results, indent=4)
    print(output)
    return output

import os
import json

def run_semgrep_analysis(dir):
    import subprocess

    # Define the Semgrep command
    semgrep_command = ['semgrep', '--config', 'auto', '--json', dir]

    
    # Run Semgrep and capture the output
    result = subprocess.run(semgrep_command, capture_output=True, text=True)
    semgrep_output = json.loads(result.stdout)
    
    # Extract specific fields from the JSON output
    findings = []
    for result in semgrep_output['results']:
        finding = {
            'check_id': result['check_id'],
            'location_path': result['path'],
            'location_start_col': result['start']['col'],
            'location_start_line': result['start']['line'],
            'lines': result['extra']['lines'],
            'message': result['extra']['message'],
            'metadata_category': result['extra']['metadata']['category'],
            'metadata_confidence': result['extra']['metadata']['confidence'],
            'metadata_cwe': result['extra']['metadata']['cwe'],
            'metadata_impact': result['extra']['metadata']['impact'],
            'metadata_owasp': result['extra']['metadata']['owasp'],
            'metadata_references': [result['extra']['metadata']['references']],
            'metadata_vulnerability_class': result['extra']['metadata']['vulnerability_class']
        }
        findings.append(finding)
    
    return findings
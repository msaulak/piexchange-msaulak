import json
from typing import Dict, Optional


class EmailTemplate:
    def __init__(self, email_template_path: str):
        self.sender: Optional[str] = None
        self.subject: Optional[str] = None
        self.mime_type: Optional[str] = None
        self.body: Optional[str] = None

        self.load_template_from_file(email_template_path)

    def load_template_from_file(self, email_template_path: str):
        with open(email_template_path) as fp_email_template:
            email_template: Dict[str, str] = json.load(fp_email_template)
            self.sender= email_template['from'] #from is a keyword in python, hence
            self.subject = email_template['subject']
            self.mime_type = email_template['mimeType']
            self.body = email_template['body']

    def __str__(self):
        ret_str_list = []
        for k,v in vars(self).items():
            ret_str_list.append(f'{k} : {v}')

        return ' | '.join(ret_str_list)

    def __repr__(self):
        return str(self)

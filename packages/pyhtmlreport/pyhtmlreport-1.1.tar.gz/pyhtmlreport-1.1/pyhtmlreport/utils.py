import os
from zipfile import ZipFile

def zip_report(module_name, report_folder):
    paths = []
    module_folder = os.path.join(report_folder, module_name)

    for root, directories, files in os.walk(module_folder):
        for file in files:
            filepath = os.path.join(root, file)
            paths.append(filepath)

    with ZipFile(os.path.join(report_folder, f'{module_name}.zip')) as z:
        for filepath in paths:
            z.write(filepath)

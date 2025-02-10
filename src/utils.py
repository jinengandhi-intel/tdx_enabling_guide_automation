import re
import requests
from src.constants import *
import subprocess
from urllib.parse import urlparse

def checkout_repo(repo_url, branch_name):
    print(f"\n\nGit clone repo: {repo_url}")
    print(f"Git checkout branch: {branch_name}")
    subprocess.run(["git", "clone", repo_url], cwd=workspace_path)
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    subprocess.run(["git", "checkout", branch_name], cwd=os.path.join(workspace_path,repo_name))

def extract_code_blocks(markdown_text):
    code_blocks = re.findall(r'```(.*?)```', markdown_text, re.DOTALL)
    return code_blocks

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_fragment_from_url(url):
    parsed_url = urlparse(url)
    return re.sub(r'\d-', '', parsed_url.fragment) 

def extract_code_blocks_after_text(markdown_text, search_text, distro=None):
    search_position = markdown_text.find(search_text)
    if search_position == -1:
        return []  # Return an empty list if the search text is not found
    text_after_search = markdown_text[search_position + len(search_text):]
    code_blocks = extract_code_blocks(text_after_search)
    if search_text not in tdx_guide_multi_commands_list:
        return code_blocks[0] if code_blocks else None  # Return the first code block if found 
    else:
        if distro == "CentOS Stream 9":
            return code_blocks[0]
        elif distro == "Ubuntu 24.04":
            return code_blocks[1]
        elif distro == "OpenSuse 15.3":
            return code_blocks[2]
        else:
            return None

def extract_links(markdown_text):
    # Regular expression to match markdown links
    link_pattern = re.compile(r'\[([^\]]+)\]\((http[^\)]+)\)')
    links = link_pattern.findall(markdown_text)
    return links

def extract_links_with_text(markdown_text, search_text):
    links = extract_links(markdown_text)
    # Filter links that contain the search text in the link text or URL
    filtered_links = [link for link in links if search_text in link[0] or search_text in link[1]]
    return filtered_links

def extract_version_from_url(url):
    # Regular expression to match the version number in the URL
    pattern = re.compile(r'/tree/([\d\.]+)')
    match = pattern.search(url)
    if match:
        return match.group(1)
    return None

def extract_commands_from_link(markdown_string, distro, url):
    if distro == "Ubuntu 24.04":
        page_section = extract_fragment_from_url(url)
        page_section = page_section.replace("-","_")
        print(f"Page section: {page_section}")
        branch = extract_version_from_url(url)
        #print(f"Extracted branch: {branch}")
        checkout_repo(canonical_repo, branch)
        canonical_readme_text = read_markdown_file(canonical_readme_path)
        command_list = f"canonical_{page_section}"
        for items in eval(command_list):
            command = extract_code_blocks_after_text(canonical_readme_text, items)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")
    else:
        checkout_repo(sig_centos_repo, sig_centos_branch)
        if "tdx/host" in url:
            sig_centos_text = read_markdown_file(sig_centos_host_os_path)
            command_list = f"sig_host"
        else:
            sig_centos_text = read_markdown_file(sig_centos_guest_os_path)
            page_section = extract_fragment_from_url(url)
            page_section = page_section.replace("-","_")
            command_list = f"sig_{page_section}"
        for items in eval(command_list):
            command = extract_code_blocks_after_text(sig_centos_text, items)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")

def run_test(distro, page, commands_dict):
    file_text = read_markdown_file(page)
    for markdown_string, markdown_type in commands_dict.items():
        if markdown_type == "link":
            print(markdown_string)
            if distro == "Ubuntu 24.04":
                distro_string = markdown_string.split()[0]
            else:
                distro_string = markdown_string.split()[1]
            print(f"Distro string {distro_string}")
            print(f"Eval of Distro string {eval(distro_string)}")
            url = extract_links_with_text(file_text, eval(distro_string))[0][1]
            print(f"url {url}")
            extract_commands_from_link(eval(distro_string), distro, url)
        else:
            command = extract_code_blocks_after_text(file_text, markdown_string, distro)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")
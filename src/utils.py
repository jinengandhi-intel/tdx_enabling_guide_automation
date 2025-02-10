import re
import requests
import select
import os
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

def run_subprocess(command, dest_dir=None, timeout=1200):
    if dest_dir:
        os.chdir(dest_dir)
    if "\\" in command:
        print("Starting Process %s from %s" %(command, os.getcwd()))
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True, timeout=timeout)
        if process.returncode != 0:
            print(process.stderr.strip())
            raise Exception("Failed to run command {}".format(command))
    else:
        command_lines = command.splitlines()
        for command in command_lines:
            command = command.strip()
            if command != "bash":
                if command.startswith("cd"):
                    print(f"Command {command}")
                    os.chdir(command.split()[1])
                    print(f"Changed directory to {os.getcwd()}")
                else:
                    print("Starting Process %s from %s" %(command, os.getcwd()))
                    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell=True, timeout=timeout)
                    if process.returncode != 0:
                        print(process.stderr.strip())
                        raise Exception("Failed to run command {}".format(command))

    try:
        if dest_dir: os.chdir(framework_path)
    except:
        print("Failed to change directory")
    
    return process.stdout.strip()

def extract_code_blocks_after_text(markdown_text, search_text, markdown_type, distro=None):
    #print(f"Search text: {search_text}")
    #print(f"Distro: {distro}")
    search_position = markdown_text.find(search_text)
    if search_position == -1:
        return []  # Return an empty list if the search text is not found
    text_after_search = markdown_text[search_position + len(search_text):]
    code_blocks = extract_code_blocks(text_after_search)
    if markdown_type != "multi_distro":
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

def extract_commands_from_link(markdown_string, distro, url, markdown_type):
    if distro == "Ubuntu 24.04":
        page_section = extract_fragment_from_url(url)
        page_section = page_section.replace("-","_")
        #print(f"Page section: {page_section}")
        branch = extract_version_from_url(url)
        #print(f"Extracted branch: {branch}")
        checkout_repo(canonical_repo, branch)
        canonical_readme_text = read_markdown_file(canonical_readme_path)
        command_list = f"canonical_{page_section}"
        for items in eval(command_list):
            command = extract_code_blocks_after_text(canonical_readme_text, items, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command).strip()
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
            command = extract_code_blocks_after_text(sig_centos_text, items, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command).strip()
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")
    return cleaned_text

def run_test(distro, page, commands_dict):
    file_text = read_markdown_file(page)
    for markdown_string, markdown_type in commands_dict.items():
        if markdown_type == "link":
            print(markdown_string)
            if distro == "Ubuntu 24.04":
                distro_string = markdown_string.split()[0]
            else:
                distro_string = markdown_string.split()[1]
            #print(f"Distro string {distro_string}")
            #print(f"Eval of Distro string {eval(distro_string)}")
            url = extract_links_with_text(file_text, eval(distro_string).split(":")[0])[0][1]
            #print(f"url {url}")
            command = extract_commands_from_link(eval(distro_string).split(":")[0], distro, url, markdown_type)
            output = run_subprocess(command, workspace_path)
            verifier_string = eval(distro_string).split(":")[1]
            

        else:
            verifier_string = markdown_string.split(":")[1]
            markdown_string = markdown_string.split(":")[0]
            command = extract_code_blocks_after_text(file_text, markdown_string, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            command = pattern.sub('', command)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {command.strip()}\n")
            output = run_subprocess(command.strip())
        
        if output:
            print("Command %s output %s" %(command, output))
        if not verifier_string:
            print(f"Verifier string {verifier_string}")
            if verifier_string not in output:
                assert False, f"Verification failed for {markdown_string}"
        else:
            if "error" in output:
                assert False, f"Verification failed for {markdown_string}"

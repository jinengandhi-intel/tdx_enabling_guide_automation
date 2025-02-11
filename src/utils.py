"""
Utility functions for TDX enabling guide automation.

This module contains various utility functions used for setting up the environment,
extracting code blocks from markdown files, running subprocess commands, and more.
"""

import re
import os
from src.constants import *
import subprocess
from urllib.parse import urlparse

def checkout_repo(repo_url, branch_name):
    """
    Clone the specified repository and checkout the specified branch.
    
    Args:
        repo_url (str): URL of the repository to clone.
        branch_name (str): Branch name to checkout.
    """
    print(f"\n\nGit clone repo: {repo_url}")
    print(f"Git checkout branch: {branch_name}")
    subprocess.run(["git", "clone", repo_url], cwd=workspace_path)
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    subprocess.run(["git", "checkout", branch_name], cwd=os.path.join(workspace_path,repo_name))

def extract_code_blocks(markdown_text):
    """
    Extract code blocks from the given markdown text.
    
    Args:
        markdown_text (str): Markdown text to extract code blocks from.
    
    Returns:
        list: List of code blocks.
    """
    code_blocks = re.findall(r'```(.*?)```', markdown_text, re.DOTALL)
    return code_blocks

def read_markdown_file(file_path):
    """
    Read the content of a markdown file.
    
    Args:
        file_path (str): Path to the markdown file.
    
    Returns:
        str: Content of the markdown file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def extract_fragment_from_url(url):
    """
    Extract the fragment part from a URL.
    
    Args:
        url (str): URL to extract the fragment from.
    
    Returns:
        str: Extracted fragment.
    """
    parsed_url = urlparse(url)
    return re.sub(r'\d-', '', parsed_url.fragment)

def extract_code_block_from_sh(file_path, start_marker, end_marker):
    """
    Extract a code block from a shell script file between specified markers.
    
    Args:
        file_path (str): Path to the shell script file.
        start_marker (str): Start marker for the code block.
        end_marker (str): End marker for the code block.
    
    Returns:
        str: Extracted code block or None if not found.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    pattern = re.compile(re.escape(start_marker) + r'(.*?)' + re.escape(end_marker), re.DOTALL)
    match = pattern.search(content)
    
    if match:
        return match.group(1).strip()
    else:
        return None
def replace_substrings(command, replacements):
    for old, new in replacements.items():
        command = command.replace(old, new)
    return command

def run_subprocess(command, dest_dir=None, timeout=1200):
    """
    Run a subprocess with the given command.
    
    Args:
        command (str): Command to run.
        dest_dir (str, optional): Directory to change to before running the command. Defaults to None.
        timeout (int, optional): Timeout for the subprocess. Defaults to 1200.
    
    Returns:
        str: Output of the subprocess.
    
    Raises:
        Exception: If the command fails.
    """
    if dest_dir:
        os.chdir(dest_dir)
    replacements = {
        "<hostname>": "sdp",
        "24.10": "24.04"
    }
    modified_command = replace_substrings(command, replacements)
    if "\\" in modified_command:
        print("Starting Process %s from %s" %(modified_command, os.getcwd()))
        process = subprocess.run(modified_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True, timeout=timeout)
        if process.returncode != 0:
            print(process.stderr.strip())
            raise Exception("Failed to run command {}".format(modified_command))
    else:
        command_lines = modified_command.splitlines()
        for each_command in command_lines:
            each_command = each_command.strip()
            if each_command != "bash":
                if each_command.startswith("cd"):
                    print(f"Command {each_command}")
                    os.chdir(each_command.split()[1])
                    print(f"Changed directory to {os.getcwd()}")
                else:
                    print("Starting Process %s from %s" %(each_command, os.getcwd()))
                    process = subprocess.run(each_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell=True, timeout=timeout)
                    print(f"Process stdout {process.stdout.strip()}")
                    if process.returncode != 0:
                        print(f"Process stderr {process.stderr.strip()}")
                        raise Exception("Failed to run command {}".format(each_command))

    try:
        if dest_dir: os.chdir(framework_path)
    except:
        print("Failed to change directory")
    
    return process.stdout.strip()

def extract_code_blocks_after_text(markdown_text, search_text, markdown_type, distro=None):
    """
    Extract code blocks that appear after a specific search text in the markdown text.
    
    Args:
        markdown_text (str): Markdown text to search in.
        search_text (str): Text to search for.
        markdown_type (str): Type of markdown (single_command, multi_distro, etc.).
        distro (str, optional): Distribution name. Defaults to None.
    
    Returns:
        list or str: Extracted code blocks or the first code block if markdown_type is not multi_distro.
    """
    print(f"Search text: {search_text}")
    print(f"Distro: {distro}")
    search_position = markdown_text.find(search_text)
    if search_position == -1:
        return []  # Return an empty list if the search text is not found
    text_after_search = markdown_text[search_position + len(search_text):]
    code_blocks = extract_code_blocks(text_after_search)
    if markdown_type != "multi_distro" and markdown_type != "read_from_other_file":
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
    """
    Extract links from the given markdown text.
    
    Args:
        markdown_text (str): Markdown text to extract links from.
    
    Returns:
        list: List of tuples containing link text and URL.
    """
    link_pattern = re.compile(r'\[([^\]]+)\]\((http[^\)]+)\)')
    links = link_pattern.findall(markdown_text)
    return links

def extract_links_with_text(markdown_text, search_text):
    """
    Extract links that contain the search text in the link text or URL.
    
    Args:
        markdown_text (str): Markdown text to search in.
        search_text (str): Text to search for in the links.
    
    Returns:
        list: List of filtered links.
    """
    links = extract_links(markdown_text)
    filtered_links = [link for link in links if search_text in link[0] or search_text in link[1]]
    return filtered_links

def extract_version_from_url(url):
    """
    Extract the version number from a URL.
    
    Args:
        url (str): URL to extract the version number from.
    
    Returns:
        str: Extracted version number or None if not found.
    """
    pattern = re.compile(r'/tree/([\d\.]+)')
    match = pattern.search(url)
    if match:
        return match.group(1)
    return None

def extract_commands_from_link(markdown_string, distro, url, markdown_type):
    """
    Extract commands from a link in the markdown string.
    
    Args:
        markdown_string (str): Markdown string to extract commands from.
        distro (str): Distribution name.
        url (str): URL to extract commands from.
        markdown_type (str): Type of markdown (single_command, multi_distro, etc.).
    
    Returns:
        dict: Dictionary of commands and their verifier strings.
    """
    command_verifier_strings = {}

    if distro == "Ubuntu 24.04":
        page_section = extract_fragment_from_url(url)
        page_section = page_section.replace("-","_")
        branch = extract_version_from_url(url)
        checkout_repo(canonical_repo, branch)
        canonical_readme_text = read_markdown_file(canonical_readme_path)
        search_list = f"canonical_{page_section}"
        print(f"Search list: {eval(search_list)}")
        for items in eval(search_list):
            verifier_string = items.split(":")[1]
            search_string = items.split(":")[0]
            command = extract_code_blocks_after_text(canonical_readme_text, search_string, markdown_type, distro)
            print(f"\ncommand: {command}")
            pattern = re.compile(r'\{.*?\}')
            cleaned_text = pattern.sub('', command).strip()
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")
            command_verifier_strings[cleaned_text]=verifier_string
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
    return command_verifier_strings

def run_test(distro, page, commands_dict):
    """
    Run the test for the given distribution and page.
    
    Args:
        distro (str): Distribution name.
        page (str): Path to the markdown page.
        commands_dict (dict): Dictionary of commands and their types.
    """
    file_text = read_markdown_file(page)
    for markdown_string, markdown_type in commands_dict.items():
        if markdown_type == "link":
            print(f"#########\nMarkdown string: {markdown_string}")
            if distro == "Ubuntu 24.04":
                distro_string = markdown_string.split()[0]
            else:
                distro_string = markdown_string.split()[1]
            print(f"Eval of Distro string {eval(distro_string)}")
            url = extract_links_with_text(file_text, eval(distro_string).split(":")[0])[0][1]
            print(f"url {url}")
            command_verifier_strings = extract_commands_from_link(eval(distro_string).split(":")[0], distro, url, markdown_type)
            for command, verifier_string in command_verifier_strings.items():
                print(f"Extracted Command from url: {command}")
                output = run_subprocess(command, workspace_path)
                if output != "":
                    print("Command %s output %s" %(command, output))
                if verifier_string != "":
                    print(f"Verifier string {verifier_string}")
                    if verifier_string.startswith("`"):
                        verifier_string = run_subprocess(verifier_string.strip("`"), workspace_path)
                    if verifier_string not in output:
                        assert False, f"Verification failed for {command.strip()}. Output doesn't match verifier string."
                else:
                    if "error" in output or "Error" in output:
                        assert False, f"Verification failed for {command.strip()}. Output contains keyword error."
        else:
            verifier_string = markdown_string.split(":")[1]
            markdown_string = markdown_string.split(":")[0]
            command = extract_code_blocks_after_text(file_text, markdown_string, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            command = pattern.sub('', command)
            print(f"Command: {command.strip()}\n")
            if markdown_type == "read_from_other_file":
                sgx_distro = command.split(":")[1]
                sgx_distro = sgx_distro.strip().strip('"')
                print(f"SGX Distro: {sgx_distro}")
                start_marker = f"# --8<-- [start:{sgx_distro}]"
                end_marker = f"# --8<-- [end:{sgx_distro}]"
                print(f"Start marker: {start_marker}")
                print(f"End marker: {end_marker}")
                command = extract_code_block_from_sh(tdx_enabling_guide_sgx_setup_script, start_marker, end_marker)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {command.strip()}\n")
            output = run_subprocess(command.strip())
            if output != "":
                print("Command %s output %s" %(command, output))
            if verifier_string != "":
                print(f"Verifier string {verifier_string}")
                if verifier_string.startswith("`"):
                    verifier_string = run_subprocess(verifier_string.strip("`"), workspace_path)
                if verifier_string not in output:
                    assert False, f"Verification failed for {command.strip()}. Output doesn't match verifier string."
            else:
                if "error" in output or "Error" in output:
                    assert False, f"Verification failed for {command.strip()}. Output contains keyword error."

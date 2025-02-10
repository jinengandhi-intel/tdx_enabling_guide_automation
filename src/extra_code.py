def extra():
    # #checkout_repo(sig_centos_repo, branch_name)
    # markdown_text = read_markdown_file(file_path)

    # for items in constants.sig_host_page:
    #     command = extract_code_blocks_after_text(markdown_text, items)
    #     # Regular expression to match text between curly braces
    #     pattern = re.compile(r'\{.*?\}')
    #     # Substitute the matched text with an empty string
    #     cleaned_text = pattern.sub('', command)
    #     print(items, cleaned_text.strip())
    
    #checkout_repo(tdx_enabling_repo, branch_name)

    markdown_text = read_markdown_file(file_path)
    search_text = "Setup Host OS"  # Replace with the actual text to search for
    links = extract_links_with_text(markdown_text, search_text)
    canonical_branch = extract_version_from_url(links[0][1])

    #checkout_repo(canonical_repo, canonical_branch)
    canonical_readme_text = read_markdown_file(canonical_readme_path)
    command = extract_code_blocks_after_text(canonical_readme_text, canonical_setup_host)
    pattern = re.compile(r'\{.*?\}')
    cleaned_text = pattern.sub('', command)
    print(f"Canonical branch: {canonical_branch}")
    print(f"Cleaned command: {cleaned_text.strip()}")


def extract_tabbed_text(markdown_text):
    # Regular expression to match lines that start with tabs or spaces
    tabbed_text_pattern = re.compile(r'^===+(.+)', re.MULTILINE)
    tabbed_text = tabbed_text_pattern.findall(markdown_text)
    return tabbed_text

def read_markdown_file_from_web(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def extract_lists(markdown_text):
    # Regular expression to match unordered lists (lines starting with '-', '*', or '+')
    unordered_list_pattern = re.compile(r'^[\*\-\+] (.+)', re.MULTILINE)
    unordered_lists = unordered_list_pattern.findall(markdown_text)

    # Regular expression to match ordered lists (lines starting with '1.', '2.', etc.)
    ordered_list_pattern = re.compile(r'^\d+\. (.+)', re.MULTILINE)
    ordered_lists = ordered_list_pattern.findall(markdown_text)

    return unordered_lists, ordered_lists

    '''file_text = read_markdown_file(tdx_enabling_guide_host_os_page)
    for markdown_string, markdown_type in host_os_commands.items():
        if markdown_type == "link":
            url = extract_links_with_text(file_text, ubuntu24_04_setup_host)
            if markdown_string == "setup_host":
                extract_setup_host_commands(ubuntu24_04_setup_host, distro, url)
        else:
            command = extract_code_blocks_after_text(file_text, markdown_string, distro)
            pattern = re.compile(r"\{.*?\}")
            cleaned_text = pattern.sub('', command)
            print(f"#########\nMarkdown string: {markdown_string}")
            print(f"Command: {cleaned_text.strip()}\n")'''
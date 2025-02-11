import re
import os
import shutil
import pytest
from src.constants import *
from src.utils import *

@pytest.fixture(scope="session", autouse=True)
def setup():
    """
    Fixture to set up the test environment.
    Deletes the existing workspace directory if it exists and creates a new one.
    Copies the required repository to the workspace.
    """
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)
    os.mkdir(workspace_path)
    #checkout_repo(tdx_enabling_repo, tdx_enabling_repo_branch)
    os.system("cp -rf /home/sdp/jinen/applications.security.confidential-computing.tdx.documentation /home/sdp/jinen/tdx_enabling_guide_automation/workspace")

def test_tdx_enabling_guide_host_setup_ubuntu24_04():
    """
    Test the TDX enabling guide for host setup on Ubuntu 24.04.
    """
    distro = "Ubuntu 24.04"
    run_test(distro, tdx_enabling_guide_host_os_page, host_setup_commands)

def test_tdx_enabling_guide_host_setup_centos_stream9():
    """
    Test the TDX enabling guide for host setup on CentOS Stream 9.
    """
    distro = "CentOS Stream 9"
    run_test(distro, tdx_enabling_guide_host_os_page, host_setup_commands)

def test_tdx_enabling_guide_guest_setup_ubuntu24_04():
    """
    Test the TDX enabling guide for guest setup on Ubuntu 24.04.
    """
    distro = "Ubuntu 24.04"
    run_test(distro, tdx_enabling_guide_guest_os_page, guest_setup_commands)

def test_tdx_enabling_guide_guest_setup_centos_stream9():
    """
    Test the TDX enabling guide for guest setup on CentOS Stream 9.
    """
    distro = "CentOS Stream 9"
    run_test(distro, tdx_enabling_guide_guest_os_page, guest_setup_commands)


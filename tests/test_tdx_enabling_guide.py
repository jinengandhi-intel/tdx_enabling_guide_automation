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
    os.system(f"sudo cp -rf /home/sdp/jinen/applications.security.confidential-computing.tdx.documentation {workspace_path}")
    print("Preparing a clean system for testing...")
    os.system("sudo apt autoremove --yes sgx-ra-service sgx-pck-id-retrieval-tool")
    os.system("sudo rm -rf /opt/intel/sgx-ra-service /opt/intel/sgx-pck-id-retrieval-tool")
    #checkout_repo(tdx_enabling_repo, tdx_enabling_repo_branch)

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

def test_tdx_enabling_infrastructure_setup_direct_registration_online_automatic_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Direct Registration online automatic on Ubuntu 24.04.
    """
    distro = "Ubuntu 24.04"
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_direct_registration_mpa_commands)

def test_tdx_enabling_infrastructure_setup_direct_registration_on_offline_manual_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Direct Registration On-/Offline manual on Ubuntu 24.04.
    """
    distro = "Ubuntu 24.04"
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_direct_registration_offline_manual_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)

def test_tdx_enabling_infrastructure_setup_indirect_registration_online_manual_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Indirect Registration Online manual on Ubuntu 24.04.
    """
    distro = "Ubuntu 24.04"
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_indirect_registration_online_manual_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)


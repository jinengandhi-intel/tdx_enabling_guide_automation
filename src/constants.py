import os

framework_path = os.getcwd()
workspace_path = os.path.join(framework_path, "workspace")

tdx_enabling_repo = "https://github.com/intel-innersource/applications.security.confidential-computing.tdx.documentation.git"
tdx_enabling_repo_branch = "internal-main"
tdx_enabling_guide_host_os_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/05/host_os_setup.md'
tdx_enabling_guide_guest_os_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/06/guest_os_setup.md'
tdx_enabling_guide_hardware_requirements = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/02/hardware_requirements.md'
tdx_enabling_guide_prerequisites = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/03/prerequisites.md'
tdx_enabling_guide_introduction = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/01/introduction.md'

canonical_repo = "https://github.com/canonical/tdx.git"
canonical_readme_path = "workspace/tdx/README.md"

sig_centos_repo = "https://gitlab.com/CentOS/virt/docs.git"
sig_centos_branch = "main"
sig_centos_host_os_path = 'workspace/docs/docs/tdx/host.md'
sig_centos_guest_os_path = 'workspace/docs/docs/tdx/guest.md'

## TDX Enabling Guide Host OS page
tdx_guide_ubuntu24_04_setup_host = "Setup Host OS:The host OS setup has been done successfully"
tdx_guide_centos_stream9_setup_host = "Configure a host"
tdx_guide_module_initialized = "Intel TDX Module is initialized:module initialized"
tdx_guide_install_msr_tools = "install the MSR Tools package:"
tdx_guide_intel_tme_enabled = "Intel TME is enabled:1"
tdx_guide_intel_tme_keys = "Intel TME keys:7f"
tdx_guide_sgx_mcheck_status = "Intel SGX and MCHECK status:0"
tdx_guide_tdx_status = "Intel TDX status:1"
tdx_guide_intel_tdx_keys = "Intel TDX keys:40"
tdx_guide_intel_sgx_package = "Intel SGX package repository:"
tdx_guide_install_qgs = "Install the QGS:"
#tdx_guide_multi_commands_list = [tdx_guide_install_msr_tools]

## Sig CentOS Host OS page
sig_tdx_package = "Virt SIG TDX package"
sig_install_tdx = "Install the TDX host packages"
start_libvirt_service = "Start libvirtd service"
sig_host = [sig_tdx_package, sig_install_tdx, start_libvirt_service]

## Canonical Ubuntu 24.04 Host OS page
canonical_setup_host = "Run the `setup-tdx-host.sh` script"
canonical_setup_host_os = [canonical_setup_host]

host_setup_commands = {"tdx_guide_ubuntu24_04_setup_host tdx_guide_centos_stream9_setup_host" : "link", \
                        tdx_guide_module_initialized : "single_command", \
                        tdx_guide_install_msr_tools : "multi_distro", tdx_guide_intel_tme_enabled : "single_command", \
                        tdx_guide_intel_tme_keys : "single_command", tdx_guide_sgx_mcheck_status : "single_command", \
                        tdx_guide_tdx_status : "single_command", tdx_guide_intel_tdx_keys : "single_command", \
                        tdx_guide_install_qgs : "multi_distro"}

## TDX Enabling Guide Guest OS page
tdx_guide_ubuntu24_04_guest_setup = "Create TD Image"
tdx_guide_centos_stream9_guest_setup = "Create VM Disk Image"
tdx_guide_ubuntu24_04_launch_td = "Boot TD"
tdx_guide_centos_stream9_launch_td = "Configure and boot VM"

## Canonical Ubuntu 24.04 Guest OS page
canonical_td_image = "TD image based on Ubuntu"
canonical_create_td_image = [canonical_td_image]

canonical_launch_td_qemu = "Boot TD with QEMU"
canonical_launch_td_virsh = "Boot TD using the following commands"
canonical_boot_td = [canonical_launch_td_qemu, canonical_launch_td_virsh]

## Sig CentOS Host OS page
sig_centos_create_td_image = "root password and an authorized SSH key"
sig_create_vm_disk_image = [sig_centos_create_td_image]

sig_centos_launch_td_qemu = "Boot a TD guest using qemu-kvm"
sig_centos_td_guest_xml = "Create the XML template file"
sig_centos_create_vm = "Create the VM using the XML template"
sig_centos_launch_td_virsh = "Start the VM"
sig_configure_and_boot_vm = [sig_centos_launch_td_qemu, sig_centos_td_guest_xml, sig_centos_create_vm, sig_centos_launch_td_virsh]

guest_setup_commands = {"tdx_guide_ubuntu24_04_guest_setup tdx_guide_centos_stream9_guest_setup" : "link", \
                        "tdx_guide_ubuntu24_04_launch_td tdx_guide_centos_stream9_launch_td" : "link"}

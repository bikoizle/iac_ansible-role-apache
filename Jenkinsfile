def BUILD_STATUS = 0;
def DATE = Calendar.getInstance().getTime().format('YYYYMMdd-hhmmss',TimeZone.getTimeZone('CET'));

def GIT_CREDS_ID = "70c6a9da-bbb3-45b8-8565-d34f227696d9";

def GIT_VMBUILD_PBK_TAG = "0.1.1";
def GIT_VMDELETE_PBK_TAG = "0.1.0";
def GIT_GETVMINFO_PBK_TAG = "0.1.3";

def GIT_URL_VMBUILD = "https://github.com/bikoizle/iac_ansible-playbook-vmbuild.git";
def GIT_URL_VMDELETE = "https://github.com/bikoizle/iac_ansible-playbook-vmdelete.git";
def GIT_URL_GETVMINFO = "https://github.com/bikoizle/iac_ansible-playbook-getvminfo.git";

def VMBUILD_PBK_DIR = "vmbuild";
def CUSTOMOS_TOML_DIR = "customos";
def VMDELETE_PBK_DIR = "vmdelete";
def GETVMINFO_PBK_DIR = "getvminfo";

def CUSTOMOS_TOML = "customos.toml"; 
def VMBUILD_PBK = "vmbuild.yml";
def VMDELETE_PBK = "vmdelete.yml";
def GETVMINFO_PBK = "getvminfo.yml";

def OS_URL = "http://bender.lan:5000/v3";
def OS_PROJECT = "admin";
def OS_PROJECT_DOMAIN = "Default";
def OS_USER_DOMAIN = "Default";
def OS_IMAGE_NAME = "CustomOS-20191207-091815";
def OS_VM_NAME = "customos_test" + "-" + "$DATE";
def OS_VM_BUILD_TIMEOUT = "200";
def OS_VM_FLAVOUR = "lab.small";
def OS_VM_NET = "private_network";

def OS_VM_INFO;

node {

     try{

        stage("Fetch files"){
    
         echo "Fetching vmbuild playbook"
    
         checkout([$class: 'GitSCM',
                branches: [[name: "refs/tags/$GIT_VMBUILD_PBK_TAG"]],
                userRemoteConfigs: [[
                    credentialsId: "$GIT_CREDS_ID",
                    url: "$GIT_URL_VMBUILD"]],
                extensions: [[$class: "RelativeTargetDirectory", relativeTargetDir: "$VMBUILD_PBK_DIR"]],
            ])
    
         echo "Fetching vmdelete playbook"
    
         checkout([$class: 'GitSCM',
                branches: [[name: "refs/tags/$GIT_VMDELETE_PBK_TAG"]],
                userRemoteConfigs: [[
                    credentialsId: "$GIT_CREDS_ID",
                    url: "$GIT_URL_VMDELETE"]],
                extensions: [[$class: "RelativeTargetDirectory", relativeTargetDir: "$VMDELETE_PBK_DIR"]],
            ])
    
         echo "Fetching getvminfo playbook"
    
         checkout([$class: 'GitSCM',
                branches: [[name: "refs/tags/$GIT_GETVMINFO_PBK_TAG"]],
                userRemoteConfigs: [[
                    credentialsId: "$GIT_CREDS_ID",
                    url: "$GIT_URL_GETVMINFO"]],
                extensions: [[$class: "RelativeTargetDirectory", relativeTargetDir: "$GETVMINFO_PBK_DIR"]],
            ])
    
        }
    
        stage("Create VM"){
    
         echo "Creating VM"
    
         withCredentials([string(credentialsId: "vault_path", variable: "vault_file")]) {
    
           ansiblePlaybook(
               playbook: "$VMBUILD_PBK_DIR/$VMBUILD_PBK",
               vaultCredentialsId: "vault_creds",
               extraVars: [
                   vault: "$vault_file",
                   url: "$OS_URL",
                   project: "$OS_PROJECT",
                   project_domain: "$OS_PROJECT_DOMAIN",
                   user_domain: "$OS_USER_DOMAIN",
                   image_name: "$OS_IMAGE_NAME",
                   vm_name: "$OS_VM_NAME",
                   timeout: "$OS_VM_BUILD_TIMEOUT",
                   vm_flavour: "$OS_VM_FLAVOUR",
                   vm_net: "$OS_VM_NET"
               ])
          }
    
        }
    
        stage("Get VM info"){
    
         echo "Getting VM info"
    
         withCredentials([string(credentialsId: "vault_path", variable: "vault_file")]) {
    
           ansiblePlaybook(
               playbook: "$GETVMINFO_PBK_DIR/$GETVMINFO_PBK",
               vaultCredentialsId: "vault_creds",
               extraVars: [
                   vault: "$vault_file",
                   url: "$OS_URL",
                   project: "$OS_PROJECT",
                   project_domain: "$OS_PROJECT_DOMAIN",
                   user_domain: "$OS_USER_DOMAIN",
                   vm_name: "$OS_VM_NAME",
                   timeout: "$OS_VM_BUILD_TIMEOUT",
               ])
          }

         echo "Loading VM info JSON file"

         OS_VM_INFO = readJSON file: "$GETVMINFO_PBK_DIR/output/vminfo.json"

        }

        stage("Run Playbook"){

          echo "Let's run!"

        }
    
        stage("Test Playbook"){
    
         echo "Removing old VM IP address ssh fingerprint"
    
         vm_ip_address = OS_VM_INFO['accessIPv4'][0]

         sh "ssh-keygen -R $vm_ip_address"
    
         echo "Running flake8 tests"
    
         sh "flake8 tests"
    
         echo "Running role tests with pytest"
    
         sh "py.test -v --hosts='ssh://root@$vm_ip_address' tests/*.py"
    
        }

    }
    catch(error){
      BUILD_STATUS = 1 
      println error.getMessage()
    }

    stage("Clean up"){

     echo "Deleting VM"

     withCredentials([string(credentialsId: "vault_path", variable: "vault_file")]) {

       ansiblePlaybook(
           playbook: "$VMDELETE_PBK_DIR/$VMDELETE_PBK",
           vaultCredentialsId: "vault_creds",
           extraVars: [
               vault: "$vault_file",
               url: "$OS_URL",
               project: "$OS_PROJECT",
               project_domain: "$OS_PROJECT_DOMAIN",
               user_domain: "$OS_USER_DOMAIN",
               vm_name: "$OS_VM_NAME",
               timeout: "$OS_VM_BUILD_TIMEOUT",
           ])
      }

      if (BUILD_STATUS == 1){

           echo "Build finished with errors!"

         }

      }

    }

}

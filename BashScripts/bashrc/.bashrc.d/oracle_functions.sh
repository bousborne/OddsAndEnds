# oracle
export OCI_CLI_AUTH=security_token

alias oci='/opt/homebrew/bin/oci'
alias oracle-oci-login="oci session authenticate --region us-ashburn-1 --profile-name DEFAULT --tenancy-name bmc_operator_access && oci session authenticate --region us-ashburn-1 --profile-name boat-session-auth --tenancy-name bmc_operator_access"
alias oracle-oci-session-authenticate="oci session authenticate --region us-ashburn-1 --profile-name DEFAULT --tenancy-name bmc_operator_access && oci session authenticate --region us-ashburn-1 --profile-name boat-session-auth --tenancy-name bmc_operator_access"
alias oracle-set-sirius-proxies="export http_proxy=http://sirius.abc.oci.oraclecloud.com:3128 && export https_proxy=http://sirius.abc.oci.oraclecloud.com:3128"
alias oracle-set-proxies="export http_proxy=http://www-proxy.us.oracle.com:80 && export https_proxy=http://www-proxy.us.oracle.com:80"

# TELESISDEV TENANCY
#alias oracle-telesisdev-ssh-thiel='ssh ubuntu@100.92.34.2'

#alias oracle-telesisdev-ssh-ansible='ssh -i ~/.ssh/android-build ubuntu@100.73.174.153'

#alias oracle-telesisdev-ssh-build-android-vm1='ssh -i ~/.ssh/telesisdev-android-build.key ubuntu@100.73.174.153'
#alias oracle-telesisdev-ssh-build-android-vm2='ssh -i ~/.ssh/telesisdev-android-build.key ubuntu@100.92.34.52'

#alias oracle-telesisdev-ssh-build-mac1='ssh-add ~/.ssh/id_rsa && ssh-add ~/.ssh/telesisdev-android-build.key && ssh -A -J ubuntu@100.73.174.153 opc@10.138.204.72 && ssh-add -D'
#alias oracle-telesisdev-ssh-build-mac2='ssh-add ~/.ssh/id_rsa && ssh-add ~/.ssh/telesisdev-android-build.key && ssh -A -J ubuntu@100.73.174.153 opc@10.138.204.74 && ssh-add -D'

#alias oracle-telesisdev-vnc-build-mac1='ssh-add ~/.ssh/id_rsa && ssh-add ~/.ssh/telesisdev-android-build.key && ssh -v -L 127.0.0.1:5900:10.138.204.72:5900 ubuntu@100.73.174.153 -N && ssh-add -D'
#alias oracle-telesisdev-vnc-build-mac2='ssh-add ~/.ssh/id_rsa && ssh-add ~/.ssh/telesisdev-android-build.key && ssh -v -L 127.0.0.1:5900:10.138.204.74:5900 ubuntu@100.73.174.153 -N && ssh-add -D'


alias sbom-db='ssh -v -N -L 3307:172.30.10.199:3306 -o ServerAliveInterval=60 ossh-softwareassurance'
# SOFTWARE ASSURANCE TENANCY
#alias oracle-softwareassurance-ssh-jb1='ssh bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com'
#alias oracle-softwareassurance-ssh-jb2='ssh bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com'

alias infra-ttp-oke-cluste='ssh -v -N -L 8443:172.30.11.31:6443 -o ServerAliveInterval=60 ossh-softwareassurance'
alias swaservices-oke-cluste='ssh -v -N -L 8443:172.30.11.118:6443 -o ServerAliveInterval=60 ossh-softwareassurance'

alias oracle-softwareassurance-ssh-socks-proxy-jb1='ssh -v -D 2222 -N bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com'
alias oracle-softwareassurance-ssh-socks-proxy-jb2='ssh -v -D 2222 -N bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com'

alias oracle-softwareassurance-ssh-artifactory-node1-jb1='ssh -J bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.3'
alias oracle-softwareassurance-ssh-artifactory-node2-jb1='ssh -J bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.66'
alias oracle-softwareassurance-ssh-artifactory-node3-jb1='ssh -J bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.53'

alias oracle-softwareassurance-ssh-artifactory-node1-jb2='ssh -J bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.3'
alias oracle-softwareassurance-ssh-artifactory-node2-jb2='ssh -J bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.66'
alias oracle-softwareassurance-ssh-artifactory-node3-jb2='ssh -J bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/artifactory_cs.key opc@172.30.10.53'

alias oracle-softwareassurance-ssh-prometheus-jb1='ssh -J bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/softwareassurance-prometheus.key opc@172.30.10.97'
alias oracle-softwareassurance-ssh-prometheus-jb2='ssh -J bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com -i /Users/bousborn/.ssh/softwareassurance-prometheus.key opc@172.30.10.97'

alias oracle-softwareassurance-k8s-port-foward-swaservices="ssh -v -N -L 50002:172.30.11.118:6443 -o ServerAliveInterval=60 bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com"
alias oracle-softwareassurance-k8s-port-foward-infra-oke="ssh -v -N -L 50000:172.30.11.119:6443 -o ServerAliveInterval=60 bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com"
alias oracle-softwareassurance-k8s-port-foward-infra-oke-ttp="ssh -v -N -L 50001:172.30.11.31:6443 -o ServerAliveInterval=60 bousborn@bydcm3cgy4d-iad.baas.ocp.oraclecloud.com"

alias vcn-mobile1='ssh -J bousborn@bzdinbrguyd-iad.baas.ocp.oraclecloud.com -i CSPROD.key opc@172.30.10.65'


#export scea_target_resource_id=ocid1.instance.oc1.iad.anuwcljtbstugdacyv7pa4toqrc45737cenwyusd4mjvz7v4sknxdlo7xbrq
#export scea_ztb_jumphost=172.30.13.249

export scea_bastion_id=ocid1.bastion.oc1.iad.amaaaaaaftkbykiag3v5p6e4csgmhzy4h4qtas3bbwspuexvneyy75ie5q3a
export scea_target_resource_id_2=ocid1.instance.oc1.iad.anuwcljtbstugdacyv7pa4toqrc45737cenwyusd4mjvz7v4sknxdlo7xbrq
export scea_ztb_jumphost_2=172.30.13.249

export scea_target_resource_id_1=ocid1.instance.oc1.iad.anuwcljrbstugdacfpyiaib4dgimtn3e2b3qo3ff2vvizcomvcqloloj764a
export scea_ztb_jumphost_1=172.30.13.248
 
export scear_bastion_id=ocid1.bastion.oc1.iad.amaaaaaaftkbykiaqzzmizodklqb65wz5kvhtoid4sbzpftxzcuts3lkn2xa
export scear_target_resource_id=ocid1.instance.oc1.iad.anuwcljrxgpweoiclwnbnpoylpje7mz6raftbejh4zwnmcxvetpe2j6grmga
export scear_ztb_jumphost=172.19.13.249
export OCI_CLI_AUTH=security_token


oracle-bastion-scea-ssh-1() {
  oracle-oci-login
  ssh-add ~/.ssh/ZTB.key
  oracle-bastion-ztb-ssh scea-1 $1
}

oracle-bastion-scea-ssh-2() {
  ssh-add ~/.ssh/id_rsa
  ssh-add ~/.ssh/instance_key_mobile_android
  ssh-add ~/.ssh/aritfactory_scea
  ssh-add ~/.ssh/okenode
  ssh-add ~/.ssh/swamobile_logrelay
  ssh-add ~/.ssh/swamobile_logrelay
  oracle-bastion-ztb-ssh scea-2 $1
}
 
oracle-bastion-scear-ssh() {
  oracle-bastion-ztb-ssh scear $1
}
 
oracle-bastion-scea-create-session() {
  oracle-bastion-ztb-create-session scea-1 ${scea_bastion_id_1} ${scea_target_resource_id_1}
}
oracle-bastion-scea-create-session() {
  oracle-bastion-ztb-create-session scea-2 ${scea_bastion_id_2} ${scea_target_resource_id_2}
}
 
oracle-bastion-scear-create-session() {
  oracle-bastion-ztb-create-session scear ${scear_bastion_id} ${scear_target_resource_id}
}
 
oracle-bastion-ztb-create-session() {
  tenancy=$1
  if [ "$tenancy" = "scea-1" ]; then
    bastion_id=${scea_bastion_id}
    target_resource_id=${scea_target_resource_id_1}
  elif [ "$tenancy" = "scea-2" ]; then
    bastion_id=${scea_bastion_id}
    target_resource_id=${scea_target_resource_id_2}
  elif [ "$tenancy" = "scear" ]; then
    bastion_id=${scear_bastion_id}
    target_resource_id=${scear_target_resource_id}
  else
    return
  fi
 
  echo Creating new session
  time oci bastion session create-managed-ssh \
  --target-os-username bousborn \
  --ssh-public-key-file ~/.ssh/id_rsa.pub \
  --bastion-id ${bastion_id} \
  --target-resource-id ${target_resource_id} \
  --session-ttl 8520 \
  --wait-for-state SUCCEEDED | tee ~/temp/bastion-${tenancy}-create-session.log
  export ZTB_SESSION_OCID=$(cat ~/temp/bastion-${tenancy}-create-session.log | jq -r '.data.resources[0].identifier')
}
 
oracle-bastion-is-session-active() {
  tenancy=$1
  export ZTB_SESSION_OCID=$(cat ~/temp/bastion-${tenancy}-create-session.log | jq -r '.data.resources[0].identifier')
  if [ -z $ZTB_SESSION_OCID ]; then
    echo no
    return
  fi
  session_state=$(oci bastion session get --session-id ${ZTB_SESSION_OCID} --query 'data."lifecycle-state"' | tr -d '"')
  if [[ $session_state == "ACTIVE" ]]; then
    echo yes
  else
    echo $session_state
  fi
}
 
oracle-bastion-ztb-get-session() {
  tenancy=$1
  [ -d ~/temp ] || mkdir ~/temp
  touch ~/temp/bastion-${tenancy}-create-session.log
  export ZTB_SESSION_OCID=$(cat ~/temp/bastion-${tenancy}-create-session.log | jq -r '.data.resources[0].identifier')
  if [[ $(oracle-bastion-is-session-active ${tenancy}) != "yes" ]]; then
    echo Session $ZTB_SESSION_OCID is not active
    oracle-bastion-ztb-create-session ${tenancy}
  else
    echo reusing last active session $ZTB_SESSION_OCID
  fi
}
 
oracle-bastion-ztb-ssh() {
  tenancy=$1
  export ZTB_SESSION_OCID=$(cat ~/temp/bastion-${tenancy}-create-session.log | jq -r '.data.resources[0].identifier')
  target_host=$2
  oracle-bastion-ztb-get-session $tenancy
  ssh-add ~/.ssh/id_rsa
  if [ "$tenancy" = "scea-1" ]; then
    ztb_jumphost=${scea_1_ztb_jumphost}
   elif [ "$tenancy" = "scea-2" ]; then
    ztb_jumphost=${scea_2_ztb_jumphost}
  elif [ "$tenancy" = "scear" ]; then
    ztb_jumphost=${scear_ztb_jumphost}
  else
    return
  fi
  if [ -z $target_host ]; then
    echo "executing: ssh -o ForwardAgent=yes -o IdentitiesOnly=yes -o ServerAliveInterval=60 -o ProxyCommand='ssh -A -p 22 ${ZTB_SESSION_OCID}@ztb.bastion.us-ashburn-1.oci.oraclecloud.com -s %h:%p' -p 22 -t ${USER}@${ztb_jumphost}"
    ssh -o ForwardAgent=yes -o IdentitiesOnly=yes -o ServerAliveInterval=60 -o ProxyCommand="ssh -A -p 22 ${ZTB_SESSION_OCID}@ztb.bastion.us-ashburn-1.oci.oraclecloud.com -s %h:%p" -p 22 -t ${USER}@${ztb_jumphost}
  else
    ssh-add ~/.ssh/${target_host}.key
    ssh -o ForwardAgent=yes -o IdentitiesOnly=yes -o ServerAliveInterval=60 -o ProxyCommand="ssh -A -p 22 ${ZTB_SESSION_OCID}@ztb.bastion.us-ashburn-1.oci.oraclecloud.com -s %h:%p" -p 22 -t ${USER}@${ztb_jumphost} ssh opc@${target_host}
  fi
  ssh-add -D
}

function oracle-telesissupport-compartment-prod-validation {
  echo "ocid1.compartment.oc1..aaaaaaaaojeoabkynzjyhuygo2l3f66gpj4d4xvl7lxfyhg7fixfgbg3dcoq"
}

function oracle-telesissupport-subnet-prod-us-iad-infra {
  echo "ocid1.subnet.oc1.iad.aaaaaaaaade2odzp6dxcvxs44g6se6q5krlqwwsnkoceopxvopllxxc4iksq"
}

oracle-validation-latest-image() {
 oci compute image list --all \
    --compartment-id `oracle-telesissupport-compartment-prod-infrastructure` \
    --lifecycle-state AVAILABLE \
    --output json | jq -r '[.data[] | select(.["display-name"] | contains("validation-image"))] | sort_by(.["time-created"]) | last | .id'
}

oracle-validation-availability-domain() {
  oci iam availability-domain list --compartment-id `oracle-telesissupport-compartment-prod-validation` --auth security_token | jq -r '.data[0].name'
}

oracle-validation-instance-launch() {
  # Run the OCI command and capture the output
  VALIDATION_INSTANCE_OUTPUT=$(oci compute instance launch --display-name "validation-SWAVCS-TICKET-NUMBER-$(id -un)-$(date +%s)" \
    --compartment-id $(oracle-telesissupport-compartment-prod-validation) \
    --shape VM.Standard3.Flex --shape-config '{"ocpus": 2, "memory": 16}' \
    --wait-for-state RUNNING \
    --image-id $(oracle-validation-latest-image) \
    --subnet-id $(oracle-telesissupport-subnet-prod-us-iad-infra) \
    --availability-domain $(oracle-validation-availability-domain) \
    --boot-volume-size-in-gbs 150 \
    --auth security_token)
  
  # Display the full output
  echo "OCI Compute Instance Launch Command Output:"
  echo "$VALIDATION_INSTANCE_OUTPUT"

  # Parse the instance ID and save it to the environment variable
  VALIDATION_INSTANCE_ID=$(echo "$VALIDATION_INSTANCE_OUTPUT" | jq -r '.data.id')

  # Confirm the instance ID
  echo "Validation Instance ID: $VALIDATION_INSTANCE_ID"
}

oracle-validation-instance-terminate() {
  oci compute instance terminate --instance-id $VALIDATION_INSTANCE_ID --preserve-boot-volume false --force
}

oracle-validation-instance-terminate-all() {
  COMPARTMENT_ID=$(oracle-telesissupport-compartment-prod-validation)

  INSTANCE_OUTPUT=$(oci compute instance list --compartment-id "$COMPARTMENT_ID" \
    --lifecycle-state RUNNING \
    --query "data[?contains(\"display-name\", '$(id -un)')].id" \
    --output json)

  if [ "$(echo "$INSTANCE_OUTPUT" | jq -r '. | length')" -eq 0 ]; then
    echo "No instances found with '$(id -un)' in their display-name."
    return 0
  fi

  VALIDATION_INSTANCE_IDS=$(echo "$INSTANCE_OUTPUT" | jq -r '.[]')

  for VALIDATION_INSTANCE_ID in $VALIDATION_INSTANCE_IDS; do
    echo "Terminating instance: $VALIDATION_INSTANCE_ID"
    oci compute instance terminate --instance-id "$VALIDATION_INSTANCE_ID" \
      --preserve-boot-volume false --force
  done

  echo "All '$(id -un)' instances terminated in compartment $COMPARTMENT_ID."
}

oracle-validation-bastion-session() {
  VALIDATION_SESSION_OUTPUT=$(oci bastion session create-port-forwarding \
  --bastion-id ocid1.bastion.oc1.iad.amaaaaaalnbwhcaaqbxwws4vl4hxnvau4ged35xedqbxts5cavr6idvkfglq \
  --display-name "$(id -un)-vnc-validation-$(date +%s)-SWASVCS-TICKET-NUMBER" \
  --target-port 5901 \
  --target-resource-id $VALIDATION_INSTANCE_ID \
  --wait-for-state SUCCEEDED \
  --ssh-public-key-file /Users/bousborne/.ssh/id_rsa.pub \
  --session-ttl 10800 \
  --auth security_token)

  echo "OCI Bastion Session Create Command Output:"
  echo "$VALIDATION_SESSION_OUTPUT"

  BASTION_SESSION_ID=$(echo "$VALIDATION_SESSION_OUTPUT" | jq -r '.data.resources[0].identifier')
  echo "Bastion session ID: $BASTION_SESSION_ID"
}

oracle-validation-ssh-tunnel() {
  ssh -i /Users/bousborn/.ssh/id_rsa -N -L 5901:172.19.18.6:5901 -p 22 "$BASTION_SESSION_ID@host.bastion.us-ashburn-1.oci.oraclecloud.com"
}


oracle-validation-begin() {
  echo "Creating instance"
  oracle-validation-instance-launch
  echo "Instance created"
  echo "Creating bastion session"
  oracle-validation-bastion-session
  echo "Bastion session created"
}

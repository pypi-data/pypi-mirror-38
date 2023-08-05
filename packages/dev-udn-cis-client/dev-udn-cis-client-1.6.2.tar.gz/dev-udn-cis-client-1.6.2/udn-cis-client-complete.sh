_udn_cis_client_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _UDN_CIS_CLIENT_COMPLETE=complete $1 ) )
    return 0
}

complete -F _udn_cis_client_completion -o default udn-cis-client;

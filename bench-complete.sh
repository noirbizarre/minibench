_bench_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _BENCH_COMPLETE=complete $1 ) )
    return 0
}

complete -F _bench_completion -o default bench;

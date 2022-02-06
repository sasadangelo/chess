PGN_FILE=""

###################################################################
# pgn2pdf()
#
# Input Parameters: none
# Description: this function deploy Spilo on IKS
# Return: none
###################################################################
pgn2pdf()
{

    python3 pgn2tex.py $PGN_FILE
    pdflatex --shell-escape ${PGN_FILE%.*}.tex
}

###################################################################
# usage
#
# Input Parameters: none
# Description: this function print the usage.
# Return: none
###################################################################
usage() {
    local RETCODE=$1

    if [ $# -gt 1 ]; then
        shift
        echo "$@"
    fi

cat - <<-EOM
Usage: $0 [OPTIONS]

When no OPTION is passed the script print this message.
OPTIONS:
    -h,  --help   Get this usage text
    -f,  --file   The PGN file to convert.
EOM
  	exit ${RETCODE}
}

###################################################################
# parse_params
#
# Input Parameters: none
# Description: this function validates the input parameters.
# Return: none
###################################################################
parse_params()
{
    local CPARM

    while [ $# -gt 0 ]; do
        CPARM=$1;
        shift
        case ${CPARM} in
        -h | --help)
            usage 0
        ;;
        -f | --file)
            PGN_FILE=$1
            shift
        ;;
        *) usage 1 "ERROR: Invalid argument $CPARM"
        ;;
        esac
    done

    if [ "$PGN_FILE" == "" ] 
    then
        echo "ERROR: specify the pgn file."
        usage
    fi

    if [ "${PGN_FILE: -4}" != ".pgn" ]
    then
        echo "ERROR: input files doesn't have a .pgn extension."
        usage
    fi

    if [ ! -f ${PGN_FILE} ]
    then
        echo "ERROR: input files doesn't exist."
        usage
    fi
}

###################################################################
# Main block
###################################################################
parse_params "$@"
pgn2pdf $PGN_FILE 

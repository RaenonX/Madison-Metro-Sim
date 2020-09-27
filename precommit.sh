# ------ Variables

CLR_RED=[31m
CLR_GRN=[32m
CLR_CYN=[36m
CLR_NC=[0m

# ------ Functions

run_cmd_exit_on_err() {
  if ! $1; then
    echo "${CLR_RED}Error @ $2${CLR_NC}"
    read -p "Press enter to continue." -r
    exit 1
  fi
}

# ------ Main

echo "${CLR_CYN}Checking with pydocstyle (metro sim)...${CLR_NC}"
run_cmd_exit_on_err "pydocstyle msnmetrosim --count" "pydocstyle check (metro sim)"

echo "${CLR_CYN}Checking with pylint (metro sim)...${CLR_NC}"
run_cmd_exit_on_err "pylint msnmetrosim" "pylint check (metro sim)"

echo "${CLR_CYN}Running code tests...${CLR_NC}"
run_cmd_exit_on_err pytest "code test"

echo "--- ${CLR_GRN}All checks passed.${CLR_NC} ---"
read -p "Press enter to continue." -r

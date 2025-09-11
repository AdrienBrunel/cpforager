#!/bin/bash

# get the directory of this bash script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# create log file
LOGFILE="$SCRIPT_DIR/run_tests.log"
> "$LOGFILE"

# define function for testing a script
run_test() {
    local test_path=$1
    local test_name=$2

    echo "Running $test_name ..." | tee -a "$LOGFILE"
    start_time=$(date +%s)
    python "$SCRIPT_DIR/$test_path" >> "$LOGFILE" 2>&1
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))
    echo "Elapsed time : $elapsed seconds" | tee -a "$LOGFILE"
    echo "" | tee -a "$LOGFILE"
}

# cd to project root in order to make os.getwd() work properly
cd $SCRIPT_DIR/..

# run all tests
echo "# ======================================================= #"
run_test "axy/test_axy.py" "test_axy.py"
run_test "axy_collection/test_axy_collection.py" "test_axy_collection.py"
run_test "gps/test_gps.py" "test_gps.py"
run_test "gps_collection/test_gps_collection.py" "test_gps_collection.py"
run_test "tdr/test_tdr.py" "test_tdr.py"
run_test "tdr_collection/test_tdr_collection.py" "test_tdr_collection.py"
run_test "gps_tdr/test_gps_tdr.py" "test_gps_tdr.py"
run_test "gps_tdr_collection/test_gps_tdr_collection.py" "test_gps_tdr_collection.py"
echo "All tests completed. Output saved to $LOGFILE."
echo "# ======================================================= #"
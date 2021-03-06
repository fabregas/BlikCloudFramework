#!/bin/sh

TEST_DB_GENERATOR=./tests/testDB.py

/usr/bin/python $TEST_DB_GENERATOR



TEST_SET="
./tests/nodesManager/friClientLibrary_test.py
./tests/nodesManager/operationsEngine_test.py
./tests/nodesManager/dbusAgent_test.py
./tests/nodesManager/nodesMonitor_test.py
./tests/nodeAgent/nodeAgent_test.py
./tests/bootManager/bootEventListener_test.py
./tests/nodeAgent/bootEventSender_test.py
./tests/nodeAgent/base_operations.py
./tests/nodesManager/base_operations.py
"

echo "Test CloudManager console..."
/usr/bin/python ./blik/console/manage.py test || exit 22

for PY in $TEST_SET ; do
    echo "* Run $PY"
    /usr/bin/python "$PY"
    rc=$?
    if [ $rc -ne 0 ] ; then
        echo "*** unit tests failed ***"
        exit $rc
    fi
done



#!/bin/bash
echo 'db.stats().ok' | mongo $1:$2/test --quiet


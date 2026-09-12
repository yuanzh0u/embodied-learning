#!/bin/sh
id="$1"
dir="/Users/eason/Documents/具身学习/work/literature-review-无本体ego-centric数据中手部检测精度对本体末端轨迹的影响-20260911"
[ -s "$dir/extractions/$id.json" ] && exit 0
SSL_CERT_FILE=/etc/ssl/cert.pem python3 /Users/eason/Documents/具身学习/work/trajacc-scratch-20260903/extract_alphaxiv_md.py --paper-id "$id" --include-full-text --cache-dir "$dir/alphaxiv-md-cache" --output "$dir/extractions/$id.json" >/dev/null 2>&1 || echo "FAIL $id"

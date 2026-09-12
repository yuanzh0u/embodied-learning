#!/bin/zsh
cd "/Users/eason/Documents/具身学习/work/literature-review-无本体ego-centric数据中手部检测精度对本体末端轨迹的影响-20260911"
export SSL_CERT_FILE=/etc/ssl/cert.pem
cat fulltext-queue-final.txt | xargs -P 4 -I {} sh -c 'test -s "extractions/{}.json" || python3 /Users/eason/Documents/具身学习/work/trajacc-scratch-20260903/extract_alphaxiv_md.py --paper-id "{}" --include-full-text --cache-dir alphaxiv-md-cache --output "extractions/{}.json" >/dev/null 2>&1 || echo "FAIL {}"'
echo DONE

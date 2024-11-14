#!/bin/bash

poetry run python upload_file.py \
 --access-key-id MwqV83TZkOH4o3S0 \
 --secret-key 73hJcxX4u4hhw865 \
 --bucket-name admin \
 --input-path README.md \
 --output-path UPLOADED_README.md

poetry run python download_file.py \
 --access-key-id MwqV83TZkOH4o3S0 \
 --secret-key 73hJcxX4u4hhw865 \
 --bucket-name admin \
 --input-path UPLOADED_README.md \
 --output-path DOWNLOADED_README.md

cat DOWNLOADED_README.md
rm DOWNLOADED_README.md
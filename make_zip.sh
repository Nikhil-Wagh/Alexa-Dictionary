rm lambda_function.zip
zip  -r lambda_function.zip . --exclude events/ --exclude  upload.sh --exclude *.git* --exclude lambda_function.pyc
echo "DONE"
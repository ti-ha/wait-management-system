#!/bin/bash
rm -rf venv
py -3.9 -m venv venv
python3 -m pip install --upgrade pip

case "$(uname -sr)" in

   Darwin*)
     source venv/bin/activate
     ;;

   Linux*Microsoft*)
     source venv/bin/activate  # Windows Subsystem for Linux
     ;;

   Linux*)
     source venv/bin/activate
     ;;

   CYGWIN*|MINGW*|MINGW32*|MSYS*)
     source venv/Scripts/activate
     ;;
     
   *)
     echo 'Other OS' 
     ;;
esac

pip3 install -r requirements.txt
deactivate

cd frontend
npm install
echo "Done"
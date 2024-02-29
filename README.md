# protein folding problem

# Run 
download files in this link
https://drive.google.com/file/d/1pYKXACVMCKPd5nOSfTGSqNLNgEauYnuh/view?usp=sharing
and together with files in this repository put them in a directory then load the docker image
```
    sudo docker load < HW2Image
    sudo  docker run -it -v ./:/Libraries --entrypoint bash chargefw2
    cd Libraries/
    cd Help/
```
and run main.py
```
    python3 main.py
```

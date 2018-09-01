# DonkeyCarDataCleaner

Start the program in the folder with the recorded data to see the image and the steering direction.

* \<space\> writes the file name to keep.txt
* Numbers 1 to 5 write the filename and a new angle between -1 and -0.2 to change.txt.
* Numbers 6 to 0 write the filename and a new angle between 0.2 and 1 to change.txt.
* b, n and m write the filename and angle 0 to change.txt (Sorry, forgot the 0 above).
* Every other key write the filename to delete.txt.
* The script also writes "status"="delete" or "keep" or "change" to the json now!
* The script continues at the first image without "status" in the json
## TODO:

* Skip files that are already in the files above.
* Improve key assignment... ;)

## Troubleshooting:

* Needs tkinter and pil package ("yaourt -S tkinter python-pillow" in arch linux).
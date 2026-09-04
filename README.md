# Delete_Duplicates

A simple terminal tool for finding and deleting duplicate files ending with `_1`.

## Requirements

You need:

* Python 3

## How to use

Download or clone this repository, then open a terminal in the project folder.

To run the program directly:

```bash
python3 delete_duplicates.py
```

To list duplicate files without deleting them:

```bash
python3 delete_duplicates.py ~/Downloads -l
```

To delete confirmed duplicate files:

```bash
python3 delete_duplicates.py ~/Downloads -f
```

You can also use the current directory:

```bash
python3 delete_duplicates.py -l
```

The program compares each `_1` file with its corresponding original file and only deletes it if the contents are identical.

## Using `ddel` as a terminal command

If you want to start the program by simply typing:

```bash
ddel
```

Run this from inside the project folder (the same folder you ran `python3 delete_duplicates.py` from earlier):

```bash
mkdir -p ~/.local/bin
ln -s "$(pwd)/delete_duplicates.py" ~/.local/bin/ddel
```

Then you can run it from any terminal:

```bash
ddel ~/Downloads -l
```

or:

```bash
ddel ~/Downloads -f
```

## Removing it

If you only downloaded the project, just delete its folder.

If you also installed the terminal command:

```bash
rm ~/.local/bin/ddel
```

Then you can delete the project folder if you want.

The files you scanned are not deleted when removing the program.

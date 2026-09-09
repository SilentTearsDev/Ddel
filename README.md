# Delete_Duplicates

A simple terminal tool for finding and deleting duplicate files while keeping the original file.

## Requirements

You need:

- Python 3

## How to use

Download or clone this repository, then open a terminal in the project folder.

To list duplicate files without deleting anything:

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

The program compares files by their contents, not just their filenames.

It recognizes common duplicate naming styles:

```text
file.txt
file_1.txt
file_2.txt
file-1.txt
file-2.txt
file (1).txt
file (2).txt
```

If the files contain exactly the same data, the file without a copy number is considered the original and is kept.

For example:

```text
photo.jpg
photo_1.jpg
photo-2.jpg
photo (3).jpg
```

If all four files are identical, `photo.jpg` is kept and the other three files are deleted.

The program only deletes numbered copies when there is a clear original file whose name does not use a recognized copy-number suffix.

If there is no clear original, the files are left untouched.

## Using `ddel` as a terminal command

If you want to start the program by simply typing:

```bash
ddel
```

First make the script executable:

```bash
chmod +x delete_duplicates.py
```

Then, from inside the project folder:

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/delete_duplicates.py" ~/.local/bin/ddel
```

Make sure `~/.local/bin` is in your PATH.

You can check with:

```bash
echo $PATH
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

Remove the terminal command with:

```bash
rm ~/.local/bin/ddel
```

Then you can delete the project folder if you want.

The files you scanned are not affected when removing the program.
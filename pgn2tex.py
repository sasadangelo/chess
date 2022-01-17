#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import chess.pgn
import chess.svg
from pprint import pprint
import argparse
import os

ARTICLE="\documentclass{article}\n"
TITLE="\\title"
AUTHOR="\\author"
DATE="\date"
BEGIN="\\begin{document}\n"
END="\end{document}\n"
SECTION="\section"
BEGIN_TITLE_PAGE="\\begin{titlepage}\n"
TITLE_PAGE="\maketitle\n"
END_TITLE_PAGE="\end{titlepage}\n"
BOLD="\\textbf"
USE_PACKAGE_SVG="\\usepackage{svg}\n"
INCLUDE_GRAPHICS="\includesvg"

# Parse the input arguments.
# The program accepts only one parameter: the PGN file name.
parser = argparse.ArgumentParser()
parser.add_argument("pgn", help="PGN file with games and variants")
args = parser.parse_args()

# Check if the file exists
if not os.path.exists(args.pgn):
    print("File " + args.pgn + " doesn't exist.")
    exit() 

# Check if the input parameter is a file
if not os.path.isfile(args.pgn):
    print("File " + args.pgn + " is not a file.")
    exit()

# Open the PGN file
pgn = open(args.pgn)

# The first page of the PFD file will contain:
# * The title
# * The author
# * The publishing date
author=""
date=""
title=""

# Load all the chapters from the PGN file
chapters = []
while True:
    chapter=chess.pgn.read_game(pgn)
    # The PGN file is divided in Chapters. In each chapter there are the following field:
    # * Chapter title
    # * Author
    # * The publishing date
    if chapter is not None:
        author=chapter.headers["Annotator"]
        date=chapter.headers["UTCDate"]
        title=chapter.headers["Event"].split(":", 2)[0]
        chapters.append(chapter)
    else: 
        break

# Create the Latex output file name
filename_wo_suffix=os.path.splitext(args.pgn)[0]
latex_filename=filename_wo_suffix + '.tex'

image_count=1
os.makedirs(filename_wo_suffix)
with open(latex_filename, 'w') as latex_file:
    latex_file.write(ARTICLE)
    if title != "":
        latex_file.write(TITLE + "{" + title + "}\n")
        latex_file.write(AUTHOR + "{" + author + "}\n")
        latex_file.write(DATE + "{" + date + "}\n")
    latex_file.write(USE_PACKAGE_SVG)
    latex_file.write(BEGIN)
    if title != "":
        latex_file.write(BEGIN_TITLE_PAGE)
        latex_file.write(TITLE_PAGE)
        latex_file.write(END_TITLE_PAGE)
    for chapter in chapters:
        chapter_title=chapter.headers["Event"].split(":", 2)[1]
        latex_file.write(SECTION + "{" + chapter_title + "}\n")
        latex_file.write("\n")
        if chapter.comment != "" :
            latex_file.write(chapter.comment.replace("\n", "\\\\"))
            latex_file.write("\\\\\n")
            latex_file.write("\\\\\n")
        board = chapter.board()
        variations = chapter.variations
        while len(variations)>0:
            board_image_filename=filename_wo_suffix + "/" + filename_wo_suffix + "_" + str(image_count) + ".svg"
            variation = variations[0]
            #pprint(variation.comment,depth=2)
            latex_file.write(INCLUDE_GRAPHICS + "[width=150pt]{" + board_image_filename + "}\n")
            latex_file.write("\\\\\n")
            latex_file.write("\\\\\n") 
            if board.turn:
                latex_file.write(BOLD + "{White " + str(board.fullmove_number) + ". " + board.san(variation.move) + "}")
            else:
                latex_file.write(BOLD + "{Black " + str(board.fullmove_number) + "... " + board.san(variation.move) + "}")
            latex_file.write("\\\\\n")
            latex_file.write("\\\\\n")
            board.push(variation.move)
            with open(board_image_filename, "w") as board_image:
                boardsvg = chess.svg.board(board=board)
                board_image.write(boardsvg)
            image_count+=1
            # print(re.sub('\[\%eval.*\]\n', '', variation.comment))
            # print("")
            #latex_file.write(variation.comment + "\\\\\n")
            latex_file.write(variation.comment.replace("\n", "\\\\"))
            latex_file.write("\\\\\n")
            latex_file.write("\\\\\n")
            variations = variation.variations
    latex_file.write(END)

# Install Pandoc on ubuntu
#```
#sudo apt install pandoc texlive-latex-recommended texlive-xetex texlive-luatex pandoc-citeproc etoolbox wkhtmltopdf
#```

# WITH EISVOGEL
#```
d=$(date +%Y-%m-%d)
fname=$1 # dGPS_with_RTKLIB
pandoc --number-sections --listings -H auto_linebreak_listings.tex \
    --variable papersize=a4paper --variable urlcolor=cyan \
    --toc -V toc-title:"Table of Contents" --variable papersize=a4paper \
    -s "$1".md -o "$1"_${d}.pdf \
    --template eisvogel
#```
#```
cp "$1"_${d}.pdf "$1".pdf
#```

## Breaks hyperlinks! Don't Use:
#gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=PebbleCounts_Manual_ebook.pdf PebbleCounts_Manual_${d}.pdf
#gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=PebbleCounts_Manual.pdf PebbleCounts_Manual_${d}.pdf
#rm -fr PebbleCounts_Manual_${d}.pdf

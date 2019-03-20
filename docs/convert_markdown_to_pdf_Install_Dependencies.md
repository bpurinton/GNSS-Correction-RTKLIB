# Install Pandoc via conda
The pandoc version available on conda is newer (and better maintained than the packages on ubuntu)

```
conda install pandoc
```
You may want to install the texlive distribution to have all fonts available (this will take some space, but it useful if you want to typeset any type of font)
```
sudo apt-get install texlive texlive-fonts-recommended texlive-fonts-extra
```

# Install Pandoc on ubuntu via package manager
```
sudo apt install pandoc texlive texlive-latex-recommended \
exlive-fonts-extra texlive-xetex texlive-luatex pandoc-citeproc etoolbox wkhtmltopdf
```

# Styles
There are different style types available for converting Markdown (md) to PDF or Latex. Here we use [eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template).

In the following, we first clone the repository, and then copy it to the standard data dir of the pandoc distribution. Alternatively, you can copy this to ~/.pandoc/template

```
cd ~
mkdir github
cd github
git clone https://github.com/Wandmalfarbe/pandoc-latex-template.git
cd pandoc-latex-template
cd ~
mkdir -p .pandoc/templates
cp -rv github/pandoc-latex-template/eisvogel.tex .pandoc/templates/eisvogel.latex
```

# Including Codes from files into Code blocks
We are using [pandoc-include-code](https://github.com/owickstrom/pandoc-include-code) to achieve this. Install stack:

```
conda install -y -c conda-forge stack 

```

Then download the code and compile (we are using stack, but you could use cabal as well):
```
cd ~/github
git clone https://github.com/owickstrom/pandoc-include-code.git
cd pandoc-include-code
stack stack.yaml
stack install
```

# Convert Markdown to PDF
(or any other format, just change filename extension)
```bash
d=$(date +%Y-%m-%d)
pandoc --number-sections --listings -H auto_linebreak_listings.tex \
    --toc -V toc-title:"Table of Contents" \
    --variable papersize=a4paper \
    --variable urlcolor=blue \
    -s PC_geomorph_roughness_manual.md -o PC_geomorph_roughness_manual_${d}.pdf \
    --template eisvogel
```

Next, convert to lower resolution PDFs with GhostScript:

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=PC_geomorph_roughness_manual_ebook.pdf PC_geomorph_roughness_manual_${d}.pdf
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=PC_geomorph_roughness_manual.pdf PC_geomorph_roughness_manual_${d}.pdf
rm -fr PC_geomorph_roughness_manual_${d}.pdf
```

BASE_NAME = report

FILES     = *.tex img/*.pdf

LATEX     = latex
PDFLATEX  = pdflatex
BIBTEX    = bibtex

pdf: $(BASE_NAME).pdf
ps: $(BASE_NAME).ps

$(BASE_NAME).pdf: $(BASE_NAME).tex
	$(PDFLATEX) -shell-escape $<
	$(BIBTEX) $(BASE_NAME)
	$(PDFLATEX) -shell-escape $<
	$(PDFLATEX) -shell-escape $<
	$(PDFLATEX) -shell-escape $<

$(BASE_NAME).ps: $(BASE_NAME).tex *.eps
	$(LATEX) $<
	$(BIBTEX) $(BASE_NAME)
	$(LATEX) $<
	$(LATEX) $<
	$(LATEX) $<

clean:
	rm -f $(BASE_NAME)*.ps $(BASE_NAME)*.dvi *.log \
	      *.aux *.blg *.toc *.brf *.ilg *.ind \
	      missfont.log $(BASE_NAME)*.bbl $(BASE_NAME)*.pdf $(BASE_NAME)*.out \
		  $(BASE_NAME)*.lof $(BASE_NAME)*.lot

all:
	make clean
	make document
	make clean
	make bitmap

document:
	latexmk -pdf -synctex=1 *.tex

clean:
	-rm *~
	-rm *.log
	-rm *.synctex.gz
	-rm *.aux
	-rm *.fdb_latexmk
	-rm *.fls

bitmap:
	for i in *.pdf; do convert -density 1200 $$i $$i.png; done


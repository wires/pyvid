all:
	rm -rf src/
	make -C ../pyvid2 clean
	mkdir src/
	cp -v ../pyvid2/* src/
	make -C ../pyvid2 all app
	cp -a ../pyvid2/dist/pyvid.app .
	zip -r pyvid.app.zip pyvid.app
	rm -rf pyvid.app
	tar cjvf pyvid2.tar.bz2 src/
	md5sum pyvid2.tar.bz2 >> pyvid2.tar.bz2.md5
	python source.py

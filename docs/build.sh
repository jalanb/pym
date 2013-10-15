#! /bin/bash


set_symbols ()
{
	SITE=~/Sites/pym
}

make_docs ()
{
	make clean > build.clean.log 2>&1
	make html > build.html.log 2>&1
	rsync -a _build/html $SITE
}

tell_user ()
{
	echo "The HTML pages are in $SITE"
}

main ()
{
	set_symbols
	make_docs
	tell_user
}

main


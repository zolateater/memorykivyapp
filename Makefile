.PHONY=all

build-android:
	buildozer android debug run	

run:
	python main.py
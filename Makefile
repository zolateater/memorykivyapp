.PHONY=all

build-android:
	buildozer android debug deploy run

run:
	python main.py
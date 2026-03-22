import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")


def main() -> None:
    from mp_search.tui.app import MPSearchApp

    app = MPSearchApp()
    app.run()


if __name__ == "__main__":
    main()

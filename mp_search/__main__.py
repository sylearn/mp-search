import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")


def main() -> None:
    args = sys.argv[1:]

    if args and args[0] == "config":
        _handle_config(args[1:])
        return

    from mp_search.tui.app import MPSearchApp

    app = MPSearchApp()
    app.run()


def _handle_config(args: list[str]) -> None:
    from mp_search.config import CONFIG_FILE, MP_API_KEY, DEFAULT_EXPORT_DIR, LANG

    if "--show" in args:
        print(f"Config file : {CONFIG_FILE}")
        print(f"  Exists    : {CONFIG_FILE.is_file()}")
        print(f"  API Key   : {'***' + MP_API_KEY[-4:] if len(MP_API_KEY) > 4 else '(not set)'}")
        print(f"  Export Dir: {DEFAULT_EXPORT_DIR}")
        print(f"  Language  : {LANG}")
        return

    if "--reset" in args:
        if CONFIG_FILE.is_file():
            CONFIG_FILE.unlink()
            print(f"Deleted {CONFIG_FILE}")
            print("Run 'mp-search' to re-configure.")
        else:
            print("No config file found.")
        return

    from mp_search.tui.app import MPSearchApp

    app = MPSearchApp(force_setup=True)
    app.run()


if __name__ == "__main__":
    main()

import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from mp_search.config import MP_API_KEY


def main() -> None:
    client = None
    if MP_API_KEY:
        from mp_search.api.client import MPClient

        try:
            client = MPClient(MP_API_KEY)
            client.connect()
        except Exception as exc:
            print(f"API 连接失败: {exc}", file=sys.stderr)

    from mp_search.tui.app import MPSearchApp

    app = MPSearchApp(client=client)
    app.run()

    if client:
        client.close()


if __name__ == "__main__":
    main()

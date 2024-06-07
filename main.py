from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from qr import QrGenerator


class TerminusQrGeneratorApp:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.create_routes()
        self.mount_dirs()

    def mount_dirs(self) -> None:
        self.app.mount("/media", StaticFiles(directory="media"), name="media")

    def create_routes(self) -> None:
        @self.app.post("/new")
        async def create_qr(
            imei: Annotated[
                str,
                Query(
                    max_length=17,
                ),
            ],
        ):
            gen = QrGenerator()
            qr = gen.create_qr(imei)
            gen.save_qr(qr, name=imei, text=f"IMEI #: {imei}")

            status = "success"
            url = f"http://api.terminusgps.com/media/{imei}.png"

            return {"status": status, "imei": imei, "url": url}

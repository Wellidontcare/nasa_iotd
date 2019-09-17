#!/bin/env python3

import requests
import textwrap
import getpass
import subprocess
import random
from pathlib import Path


def main():
    key = ""
    url = f"https://api.nasa.gov/planetary/apod?api_key={key}"
    response = requests.get(url)
    json_response = response.json()

    user = getpass.getuser()

    date = json_response["date"]
    explanation = json_response["explanation"]
    img_url = json_response["hdurl"]
    formated_explanation = textwrap.fill(explanation)
    image = requests.get(img_url)
    image_path = (
        Path.home() / "Downloads" / ("IOTD" + str(random.randint(0, 20)) + ".jpg")
    )
    with open(image_path, "wb") as image_file:
        for chunk in image.iter_content(1024):
            image_file.write(chunk)

    with open(Path.home() / "Downloads" / "Description.txt", "w") as description:
        description.write(formated_explanation)

    print("\n" + formated_explanation + "\n")
    print(date + "\n")
    print("\n" + img_url)

    subprocess.run(
        [
            "dbus-send",
            "--session",
            "--dest=org.kde.plasmashell",
            "--type=method_call",
            "/PlasmaShell",
            "org.kde.PlasmaShell.evaluateScript",
            'string: var Desktops = desktops();for (i=0;i<Desktops.length;i++) {d = Desktops[i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");d.writeConfig("Image", "file:'
            + image_path.as_posix()
            + '");}',
        ]
    )

    print("\n\nDescription and image-file can be found in the Downloads folder")

    quit()


if __name__ == "__main__":
    main()

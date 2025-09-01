## How to Set Up the Eye Tracker
1. Make sure that you have the [EyeLink Developers Kit](https://www.sr-research.com/support/docs.php?topic=linuxsoftware) installed
2. Install the correct version of PyLink using the following command: `python3.12 -m pip install --index-url=https://pypi.sr-support.com sr-research-pylink`
3. If the above command did not work, install the **whl** file located in the 'File' folder using the following command (replace `*.whl` with the actual file path where you've downloaded the wheel file): `python3.12 -m pip install <file_path>.whl`
4. Use the eye tracker using the functions provided in the `eyelink.py` file.

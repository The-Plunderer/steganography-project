import subprocess
import sys
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


def run_cli(*args):
    return subprocess.run(
        [PYTHON, "src/steg.py", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )


def create_test_images(tmp_path):
    cover_path = tmp_path / "cover.png"
    secret_path = tmp_path / "secret.png"

    cover = Image.new("RGB", (20, 20), "white")
    secret = Image.new("RGB", (5, 5), "red")

    cover.save(cover_path)
    secret.save(secret_path)

    return cover_path, secret_path


def test_cli_help():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "image-encode" in result.stdout
    assert "image-decode" in result.stdout


def test_cli_lsb332_encode_decode(tmp_path):
    cover_path, secret_path = create_test_images(tmp_path)

    stego_path = tmp_path / "lsb_stego.png"
    recovered_path = tmp_path / "lsb_recovered.png"

    encode_result = run_cli(
        "image-encode",
        "--method", "lsb332",
        "--cover", str(cover_path),
        "--secret", str(secret_path),
        "--output", str(stego_path)
    )

    assert encode_result.returncode == 0
    assert stego_path.exists()

    decode_result = run_cli(
        "image-decode",
        "--method", "lsb332",
        "--image", str(stego_path),
        "--output", str(recovered_path)
    )

    assert decode_result.returncode == 0
    assert recovered_path.exists()

    recovered = Image.open(recovered_path)
    assert recovered.size == (5, 5)


def test_cli_spiral332_encode_decode(tmp_path):
    cover_path, secret_path = create_test_images(tmp_path)

    stego_path = tmp_path / "spiral_stego.png"
    recovered_path = tmp_path / "spiral_recovered.png"

    encode_result = run_cli(
        "image-encode",
        "--method", "spiral332",
        "--cover", str(cover_path),
        "--secret", str(secret_path),
        "--output", str(stego_path)
    )

    assert encode_result.returncode == 0
    assert stego_path.exists()

    decode_result = run_cli(
        "image-decode",
        "--method", "spiral332",
        "--image", str(stego_path),
        "--output", str(recovered_path)
    )

    assert decode_result.returncode == 0
    assert recovered_path.exists()

    recovered = Image.open(recovered_path)
    assert recovered.size == (5, 5)
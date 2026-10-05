import numpy as np

from src.adaptive332 import (
    choose_embedding_channel,
    set_indicator,
    get_indicator,
    select_channel,
    embed_adaptive_pixel,
    extract_adaptive_pixel,
)


def test_green_channel_selection():
    cover = np.array(
        [100, 50, 100],
        dtype=np.uint8
    )

    assert choose_embedding_channel(cover) == "green"


def test_blue_channel_selection():
    cover = np.array(
        [100, 150, 80],
        dtype=np.uint8
    )

    assert choose_embedding_channel(cover) == "blue"


def test_green_indicator():
    red = set_indicator(
        255,
        "green"
    )

    assert get_indicator(red) == 0b00
    assert select_channel(red) == "green"


def test_blue_indicator():
    red = set_indicator(
        255,
        "blue"
    )

    assert get_indicator(red) == 0b01
    assert select_channel(red) == "blue"


def test_green_adaptive_embedding():
    cover = np.array(
        [100, 50, 100],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    assert select_channel(
        stego[0]
    ) == "green"


def test_blue_adaptive_embedding():
    cover = np.array(
        [100, 150, 80],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    assert select_channel(
        stego[0]
    ) == "blue"


def test_green_indicator_survives_embedding():
    cover = np.array(
        [100, 50, 100],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    assert get_indicator(
        stego[0]
    ) == 0b00


def test_blue_indicator_survives_embedding():
    cover = np.array(
        [100, 150, 80],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    assert get_indicator(
        stego[0]
    ) == 0b01


def test_green_adaptive_round_trip():
    cover = np.array(
        [100, 50, 100],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    recovered = extract_adaptive_pixel(
        stego
    )

    expected = np.array(
        [128, 160, 64],
        dtype=np.uint8
    )

    assert np.array_equal(
        recovered,
        expected
    )


def test_blue_adaptive_round_trip():
    cover = np.array(
        [100, 150, 80],
        dtype=np.uint8
    )

    secret = np.array(
        [255, 175, 95],
        dtype=np.uint8
    )

    stego = embed_adaptive_pixel(
        cover,
        secret
    )

    recovered = extract_adaptive_pixel(
        stego
    )

    expected = np.array(
        [128, 160, 80],
        dtype=np.uint8
    )

    assert np.array_equal(
        recovered,
        expected
    )
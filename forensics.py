
import hashlib
import io
import json
import os
from datetime import datetime, timezone

import numpy as np
from PIL import Image, ExifTags, ImageChops, ImageEnhance


def calculate_hash(file_bytes, algorithm="sha256"):
    """Calculate a cryptographic hash of the original file bytes."""
    return hashlib.new(algorithm, file_bytes).hexdigest()


def extract_metadata(image):
    """Extract basic image information and available EXIF tags."""
    metadata = {
        "format": image.format,
        "width": image.width,
        "height": image.height,
        "color_mode": image.mode,
        "exif": {}
    }

    try:
        exif_data = image.getexif()

        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(
                tag_id, str(tag_id)
            )

            # Convert values into JSON-compatible representations.
            if isinstance(value, bytes):
                value = f"<binary data: {len(value)} bytes>"
            elif not isinstance(value, (str, int, float, bool)):
                value = str(value)

            metadata["exif"][tag_name] = value

    except Exception as error:
        metadata["exif_error"] = str(error)

    return metadata


def perform_ela(image, quality=90):
    """
    Perform Error Level Analysis (ELA) for JPEG images.

    Returns a difference image for visual inspection.
    ELA is an indicator, not proof of manipulation.
    """
    rgb_image = image.convert("RGB")

    buffer = io.BytesIO()
    rgb_image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    with Image.open(buffer) as compressed:
        recompressed = compressed.convert("RGB")

    difference = ImageChops.difference(
        rgb_image, recompressed
    )

    extrema = difference.getextrema()
    max_difference = max(
        channel_max for _, channel_max in extrema
    )

    if max_difference > 0:
        difference = ImageEnhance.Brightness(
            difference
        ).enhance(255.0 / max_difference)

    return difference


def calculate_pixel_statistics(image):
    """Calculate basic pixel intensity statistics."""
    pixels = np.asarray(image.convert("RGB"))

    return {
        "mean_intensity": round(float(np.mean(pixels)), 4),
        "minimum_intensity": int(np.min(pixels)),
        "maximum_intensity": int(np.max(pixels))
    }


def analyze_image(file_bytes, filename):
    """
    Analyze an uploaded image.

    Returns a dictionary containing the decoded image,
    metadata, hashes, pixel statistics, and ELA results.
    """
    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    try:
        with Image.open(io.BytesIO(file_bytes)) as source:
            source.load()
            image = source.copy()
            image_format = source.format
    except Exception as error:
        raise ValueError(
            "The file is not a valid supported image."
        ) from error

    # Preserve the detected format after copying.
    image.format = image_format

    metadata = extract_metadata(image)

    hashes = {
        "MD5": calculate_hash(file_bytes, "md5"),
        "SHA256": calculate_hash(file_bytes, "sha256")
    }

    pixel_statistics = calculate_pixel_statistics(image)

    ela_image = None

    if image_format == "JPEG":
        ela_image = perform_ela(image)

    return {
        "filename": os.path.basename(filename),
        "file_size_bytes": len(file_bytes),
        "image": image,
        "metadata": metadata,
        "hashes": hashes,
        "pixel_statistics": pixel_statistics,
        "ela_image": ela_image
    }


def generate_report(results):
    """Create a JSON-serializable forensic report."""
    return {
        "tool": "Digital Image Forensics Tool",
        "analysis_time_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "filename": results["filename"],
        "file_size_bytes": results["file_size_bytes"],
        "file_hashes": results["hashes"],
        "image_metadata": results["metadata"],
        "pixel_statistics": results["pixel_statistics"],
        "ela": {
            "performed": results["ela_image"] is not None,
            "note": (
                "ELA highlights compression differences. "
                "It does not independently prove manipulation."
            )
        }
    }


def export_report_json(report):
    """Convert the report to downloadable JSON bytes."""
    return json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    ).encode("utf-8")

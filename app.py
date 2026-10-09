
import streamlit as st

from forensics import analyze_image, generate_report, export_report_json


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Digital Image Forensics",
    page_icon="🔍",
    layout="wide"
)

st.title("Digital Image Forensics Tool")

st.write(
    "Upload an image to examine its metadata, file hashes, "
    "pixel statistics, and possible JPEG compression anomalies."
)

st.warning(
    "Forensic indicators are not proof of manipulation. "
    "Analyze evidence responsibly."
)


# -------------------------------
# IMAGE UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "tif", "tiff", "bmp", "webp"]
)

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    try:
        # Call the main logic from forensics.py.
        results = analyze_image(
            file_bytes,
            uploaded_file.name
        )

        image = results["image"]

        # -------------------------------
        # IMAGE INFORMATION
        # -------------------------------

        st.subheader("1. Image Information")

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                image,
                caption="Uploaded image",
                use_container_width=True
            )

        with col2:
            st.write("**Filename:**", results["filename"])
            st.write(
                "**File size:**",
                f'{results["file_size_bytes"]:,} bytes'
            )
            st.write(
                "**Format:**",
                results["metadata"]["format"]
            )
            st.write(
                "**Dimensions:**",
                f'{image.width} × {image.height}'
            )
            st.write("**Color mode:**", image.mode)

        # -------------------------------
        # HASH ANALYSIS
        # -------------------------------

        st.subheader("2. File Integrity Hashes")

        st.caption(
            "Record these hashes when acquiring evidence "
            "and compare them later to check file integrity."
        )

        st.text_input(
            "MD5",
            value=results["hashes"]["MD5"],
            disabled=True
        )

        st.text_input(
            "SHA-256",
            value=results["hashes"]["SHA256"],
            disabled=True
        )

        # -------------------------------
        # METADATA
        # -------------------------------

        st.subheader("3. Metadata Analysis")

        metadata = results["metadata"]
        st.json(metadata)

        if metadata["exif"]:
            st.success("EXIF metadata is available.")
        else:
            st.info(
                "No standard EXIF tags were found. "
                "This does not mean the image is manipulated."
            )

        # -------------------------------
        # ERROR LEVEL ANALYSIS
        # -------------------------------

        st.subheader("4. Error Level Analysis (ELA)")

        ela_image = results["ela_image"]

        if ela_image is not None:

            col3, col4 = st.columns(2)

            with col3:
                st.image(
                    image.convert("RGB"),
                    caption="Original image",
                    use_container_width=True
                )

            with col4:
                st.image(
                    ela_image,
                    caption="ELA visualization",
                    use_container_width=True
                )

            st.caption(
                "Bright regions show larger compression differences. "
                "Editing, image content, and compression history can "
                "all cause differences. Investigate alongside other evidence."
            )

        else:
            st.info(
                "ELA is available in this prototype only for "
                "images identified as JPEG."
            )

        # -------------------------------
        # PIXEL STATISTICS
        # -------------------------------

        st.subheader("5. Pixel Statistics")

        statistics = results["pixel_statistics"]

        col5, col6, col7 = st.columns(3)

        col5.metric(
            "Mean intensity",
            f'{statistics["mean_intensity"]:.2f} / 255'
        )

        col6.metric(
            "Minimum intensity",
            statistics["minimum_intensity"]
        )

        col7.metric(
            "Maximum intensity",
            statistics["maximum_intensity"]
        )

        # -------------------------------
        # FORENSIC REPORT
        # -------------------------------

        st.subheader("6. Download Forensic Report")

        report = generate_report(results)
        report_bytes = export_report_json(report)

        st.download_button(
            label="Download JSON Report",
            data=report_bytes,
            file_name="image_forensic_report.json",
            mime="application/json"
        )

        st.success("Image analysis completed.")

    except (ValueError, OSError) as error:
        st.error(f"Unable to analyze the image: {error}")

    except Exception as error:
        st.error(
            f"An unexpected error occurred: {error}"
        )

else:
    st.info("Upload an image to start the analysis.")

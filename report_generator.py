import tempfile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def create_pdf(results):

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(tmp.name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Baseplate Anchor Design Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    for key, value in results.items():

        content.append(
            Paragraph(
                f"<b>{key}</b> : {value}",
                styles["Normal"]
            )
        )

    doc.build(content)

    return tmp.name

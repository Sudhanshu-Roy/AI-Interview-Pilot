from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

import io


def generate_pdf_report(
    analysis,
    scorecard
):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Interview Pilot Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Resume Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            analysis.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Interview Scorecard",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            scorecard.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer
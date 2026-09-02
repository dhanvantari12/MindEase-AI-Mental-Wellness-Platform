"""
Journal PDF export utilities.
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from features.journal.services import (
    get_user_journal_entries,
)


def export_journal_pdf(
    user_id: str,
    output_path: str,
):
    """
    Export all journal entries
    to a PDF file.
    """

    entries = get_user_journal_entries(
        user_id
    )

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "MindEase Journal",
            styles["Title"],
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    if not entries:

        elements.append(
            Paragraph(
                "No journal entries found.",
                styles["Normal"],
            )
        )

    else:

        for entry in entries:

            date_text = (
                entry.created_at.strftime(
                    "%d %B %Y"
                )
            )

            elements.append(
                Paragraph(
                    date_text,
                    styles["Heading3"],
                )
            )

            elements.append(
                Paragraph(
                    entry.content,
                    styles["BodyText"],
                )
            )

            elements.append(
                Spacer(1, 12)
            )

    doc.build(elements)

    return output_path
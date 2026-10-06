import re

import streamlit as st


st.set_page_config(
    page_title="Spam Message Detector",
    page_icon="🛡️",
    layout="centered",
)

SPAM_PATTERNS = [
    (r"\b(free|winner|won|prize|reward|gift card|lottery)\b", 2),
    (r"\b(claim|claim now|act now|limited time|urgent|final warning)\b", 2),
    (
        r"\b(click here|click this link|verify your (account|password|login)|"
        r"update payment)\b",
        3,
    ),
    (
        r"\b(guaranteed income|earn money|make thousands|instant loan|"
        r"no experience needed)\b",
        2,
    ),
    (
        r"\b(send|share) (your )?(password|otp|account details|bank details)\b",
        4,
    ),
    (r"https?://|www\.", 1),
    (
        r"\b(inaam jeeta|prize lene|abhi apply|guaranteed income|"
        r"details bhejein)\b",
        2,
    ),
    (
        r"\b(account is blocked|account will be suspended|"
        r"account band ho jayega)\b",
        2,
    ),
]

EXAMPLES = {
    "Prize message": (
        "Congratulations! You won a free iPhone. "
        "Claim now by clicking this link."
    ),
    "Normal message": "Hey, are we still meeting for lunch today?",
    "Hinglish example": (
        "Aapne inaam jeeta hai, prize lene ke liye link par click karein."
    ),
}


def check_message(message: str) -> int:
    """Return a simple spam-pattern score for the given message."""
    return sum(
        weight
        for pattern, weight in SPAM_PATTERNS
        if re.search(pattern, message, flags=re.IGNORECASE)
    )


st.title("🛡️ Spam Message Detector")
st.write("Paste a message below to check for common spam signals.")

st.info(
    "This is a simple educational demo. It uses keyword patterns, "
    "not a trained AI model. Its result is only a hint."
)

if "message_text" not in st.session_state:
    st.session_state.message_text = ""

st.text_area(
    "Paste your message",
    key="message_text",
    height=160,
    max_chars=5000,
    placeholder=(
        "Example: Congratulations! You have won a free prize. "
        "Claim it now..."
    ),
)

st.caption(
    "Your message is checked locally by this app and is not sent to an API."
)

example_columns = st.columns(len(EXAMPLES))
for column, (label, example) in zip(example_columns, EXAMPLES.items()):
    if column.button(label, use_container_width=True):
        st.session_state.message_text = example
        st.rerun()

if st.button("Check message", type="primary", use_container_width=True):
    message = st.session_state.message_text.strip()

    if not message:
        st.warning("Please paste a message first.")
    else:
        score = check_message(message)

        if score >= 3:
            st.error("⚠️ Possible spam")
            st.write(
                "This message contains common spam signals. Avoid clicking "
                "links or sharing personal details unless you verify the sender."
            )
        else:
            st.success("✅ No obvious spam signals")
            st.write(
                "This checker did not find strong spam patterns. "
                "That does not guarantee the message is safe."
            )

        st.caption(f"Demo pattern score: {score}")

with st.expander("How this demo works"):
    st.markdown(
        """
        The app checks for phrases often found in suspicious messages, such
        as prize claims, urgent requests, suspicious links, and requests for
        passwords or account details.

        This is a basic rule-based demo. A real spam detector would need a
        larger, representative message dataset and proper model evaluation.
        """
    )
import gradio as gr
import detective as d


def investigate(text):
    # Gradio calls this function every time the text changes.
    # It returns one value for each output below, in the same order.
    if not text.strip():
        return {}, "Type or paste a message above."
    ranking = d.rank_languages(text)
    verdict = d.detect(text)
    if verdict == "Unknown":
        report = "### Verdict: Unknown\nNot enough evidence. Try a longer message."
    else:
        evidence = d.clues(text, verdict, n=8)
        report = f"### Verdict: {verdict}\n**Evidence** (shared 3-letter chunks): " + "  ".join(f"`{g.replace(' ', '_')}`" for g in evidence)
    return dict(ranking), report


def languages_known():
    # Shown on the second tab: one line per language the detective has learned.
    lines = [f"- **{name}**: {len(profile)} different 3-letter chunks" for name, profile in d.PROFILES.items()]
    return f"The detective knows **{len(d.PROFILES)}** languages:\n\n" + "\n".join(lines)


with gr.Blocks(title="Language Detective") as demo:
    gr.Markdown("# Language Detective")
    with gr.Tab("Investigate"):
        text = gr.Textbox(lines=3, label="Mystery message")
        report = gr.Markdown()
        scores = gr.Label(num_top_classes=10, label="Fingerprint match for every language")
        gr.Examples([["Je voudrais un croissant et un chocolat chaud, s'il vous plait."],
                     ["Yaar aaj bahut garmi hai, chalo ice cream khaane chalte hain."],
                     ["la pasta e buona"], ["pizza"]], inputs=text)
    with gr.Tab("Languages I know"):
        known = gr.Markdown()

    text.change(investigate, text, [scores, report])
    demo.load(languages_known, None, known)

if __name__ == "__main__":
    demo.launch()
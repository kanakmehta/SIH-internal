import nltk
import gradio as gr
from PIL import Image
import torch
from torchvision import transforms, models

# --- NLTK setup ---
nltk.download("punkt")
nltk.download("wordnet")

from nltk.tokenize import sent_tokenize

# --- Sample text (for demo) ---
raw_doc = """Hello! Kisaan Sathi yahan hai. Aapki kis prashn mein madad karun?"""
sent_tokens = sent_tokenize(raw_doc.lower())
print(sent_tokens)

# --- Pretrained ResNet for demo (not real crop disease detection) ---
model = models.resnet18(pretrained=True)
model.eval()
class_names = ["Healthy", "Leaf Rust", "Blight", "Powdery Mildew"]

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def detect_crop_disease(image):
    img = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
    _, pred = torch.max(outputs, 1)
    disease = class_names[pred.item() % len(class_names)]  # Demo mapping

    if disease == "Healthy":
        return "✅ Your crop looks healthy! Keep following good farming practices."
    else:
        return f"🛡️ Detected: {disease}. Please take appropriate measures."

# --- Chatbot logic ---
def kisaan_ai(user_query):
    query = user_query.lower()
    if "driver" in query or "operator" in query:
        return "🚜 Agar aap machine drive nahi kar sakte, to trained driver/operator ke sath rented equipment provide kiya ja sakta hai."
    elif "equipment" in query or "machine" in query:
        return "📌 Suggestion Box guide karta hai ki crop ke liye kaunsa equipment use karna chahiye. Agar multi-purpose machine kaam aa sakti hai, to cost aur effort dono bachate hain."
    elif "paani" in query or "water" in query or "irrigation" in query:
        return "💧 Irrigation aur rainwater harvesting se paani ki bachat hoti hai. Excess ya kam paani ke liye app me alerts bhi milenge."
    elif "yojna" in query or "scheme" in query or "sarkari" in query:
        return "📑 Govt. Schemes & Updates feature se aap latest schemes, subsidies aur benefits ke baare me jaan sakte hain aur PM-Kisan ya KCC ke through apply kar sakte hain."
    elif "disease" in query or "pest" in query or "crop health" in query:
        return "🛡️ Crop Disease & Pest Detection feature early detect karta hai aur suitable solution ya medicines suggest karta hai."
    elif "namaste" in query or "hello" in query:
        return "🙏 Namaste! Kisaan Sathi aapki madad ke liye tayar hai."
    elif "dhanyavaad" in query or "thank" in query:
        return "🤝 Dhanyavaad! Hum hamesha aapke saath hain."
    else:
        return "Maaf kijiye, mujhe samajh nahi aaya. Kripya apna prashn alag tareeke se puchhein."

quick_questions = [
    "Mujhe driver/operator ki zarurat hai",
    "Kaunsa equipment use karna chahiye?",
    "Paani ki samasya kaise solve karein?",
    "Sarkari yojnaon ka labh kaise lein?",
    "Crop diseases aur pests kaise detect karein?"
]

def chat_fn(user_message, history):
    reply = kisaan_ai(user_message)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    return history, ""

def image_query(image, history):
    reply = detect_crop_disease(image)
    history.append({"role": "user", "content": "🖼️ Image Uploaded"})
    history.append({"role": "assistant", "content": reply})
    return history

def clear_chat():
    return [], ""

# --- Custom CSS ---
custom_css = """
.gradio-container {
    background: linear-gradient(to bottom right, #e6f7e6, #fff9e6) !important;
}
h1, h3 {
    color: #2e7d32;
}
.chatbot {
    background-color: #ffffff !important;
    border: 3px solid #fbc02d;
    border-radius: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}
.quick-btns button {
    margin: 5px;
    background-color: #81c784;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 12px;
    cursor: pointer;
}
.quick-btns button:hover {
    background-color: #66bb6a;
}
"""

# --- Gradio App ---
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        <div style='text-align: center;'>
            <h1>🌾 Kisaan AI – आपका कृषि सहायक</h1>
            <p style="color:#388e3c;">Apne prashn puchhiye, quick question select karein ya crop image upload karein!</p>
        </div>
        """
    )

    chatbot = gr.Chatbot(label="Kisaan AI Chat", elem_classes="chatbot", height=400, type="messages")
    msg = gr.Textbox(placeholder="Yahaan apna prashn likhiye...", lines=1)
    img_input = gr.Image(type="pil", label="Upload Image for Crop Disease Detection")

    # Text input
    msg.submit(chat_fn, [msg, chatbot], [chatbot, msg])

    # Clear chat button
    clear_btn = gr.Button("🗑️ Clear Chat", elem_classes="quick-btns")
    clear_btn.click(clear_chat, inputs=[], outputs=[chatbot, msg])

    # Quick question buttons
    with gr.Row(elem_classes="quick-btns"):
        for q in quick_questions:
            btn = gr.Button(q)
            btn.click(lambda history, query=q: chat_fn(query, history),
                      inputs=[chatbot],
                      outputs=[chatbot, msg])

    # Image upload
    img_input.change(image_query, [img_input, chatbot], [chatbot])

demo.launch(share=True)

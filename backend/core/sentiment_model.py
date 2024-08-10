import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoTokenizer, AutoModel
from torch.nn import TransformerEncoder, TransformerEncoderLayer

feelings = ["Happy", "Angry", "Anxious", "Ashamed", "Disappointed", "Disgusted", "Envious", "Guilty", "Insecure", "Loving", "Sad", "Jealous"]
feelings1 = ["خوشحال", "عصبانی", "نگران", "شرمنده", "ناامید", "متنفر", "حریص", "گناهکار", "ناامن", "عاشق", "ناراحت", "حسود"]
feelings2 = ["خوشحالی", "عصبانیت", "نگرانی", "شرمندگی", "ناامیدی", "تنفر", "حریص‌ بودن", "گناهکاری", "ناامن‌بودن", "عشق", "ناراحتی", "حسادت"]

tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")
embedding_model = AutoModel.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")

class SimpleTransformerClassifier(nn.Module):
    def __init__(self, input_dim, output_dim, nhead=16, nhid=64, dropout=0.5):
        super().__init__()
        self.model_type = 'Transformer'
        self.src_mask = None

        self.encoder_layer = TransformerEncoderLayer(d_model=input_dim, nhead=nhead, dim_feedforward=nhid, dropout=dropout)
        self.transformer_encoder = TransformerEncoder(self.encoder_layer, num_layers=1)
        self.classifier = nn.Linear(input_dim, output_dim)

    def forward(self, src):
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device
            mask = self._generate_square_subsequent_mask(len(src)).to(device)
            self.src_mask = mask

        output = self.transformer_encoder(src, self.src_mask)
        output = self.classifier(output)
        return output

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

def predict_sentiment(sentiment_model, sentence):
    embedding = generate_embedding(sentence)

    sentence_tensor = torch.tensor(embedding)
    sentence_tensor = sentence_tensor.unsqueeze(0)
    sentence_tensor = sentence_tensor.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    sentiment_model.eval()
    with torch.no_grad():
        output = model(sentence_tensor)

    probabilities = F.softmax(output, dim=1)
    _, predicted_label = torch.max(probabilities, dim=1)
    predicted_label = predicted_label.item()
    return feelings[predicted_label], feelings1[predicted_label], feelings2[predicted_label]

def generate_embedding(sentence):
    tokens = tokenizer.tokenize(sentence)
    input_ids = torch.tensor([tokenizer.convert_tokens_to_ids(tokens)])

    with torch.no_grad():
        outputs = embedding_model(input_ids)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze()

    return embedding.tolist()

input_dim = 768
output_dim = 12

model = SimpleTransformerClassifier(input_dim, output_dim)
model_weights = torch.load('core/model_weights.pth')
model.load_state_dict(model_weights)
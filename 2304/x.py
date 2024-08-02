import random 
import torch 
from transformers import BertTokenizer, BertModel 
from sklearn.metrics.pairwise import cosine_similarity

seed = 42 
random.seed(seed)
torch.manual_seed(seed)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
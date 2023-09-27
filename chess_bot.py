from peewee import *
import base64
import os
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, IterableDataset, random_split
import pytorch_lightning as pl
from random import randrange
import time
from collections import OrderedDict
from torch.utils.tensorboard import SummaryWriter
import fen2BB
db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')

class Evaluations(Model):
  id = IntegerField()
  fen = TextField()
  binary = BlobField()
  eval = FloatField()

  class Meta:
    database = db

  def binary_base64(self):
    return base64.b64encode(self.binary)


class EvaluationDataset(IterableDataset):
  def __init__(self, count):
    self.count = count
  def __iter__(self):
    return self
  def __next__(self):
    idx = randrange(self.count)
    return self[idx]
  def __len__(self):
    return self.count
  def __getitem__(self, idx):
    eval = Evaluations.get(Evaluations.id == idx+1)
    bin = fen2BB.fen2BB(eval.fen)
    eval.eval = max(eval.eval, -15)
    eval.eval = min(eval.eval, 15)
    ev = np.array([eval.eval]).astype(np.single) 
    return {'binary':bin, 'eval':ev}    
  def __getitemorg__(self, idx):
    eval = Evaluations.get(Evaluations.id == idx+1)
    return eval
  def __getitembinpacked__(self, idx):
    eval = Evaluations.get(Evaluations.id == idx+1)
    bin = np.frombuffer(eval.binary, dtype=np.uint8)
    return bin
  
class EvaluationModel(pl.LightningModule):
  def __init__(self,learning_rate=1e-3,batch_size=512,layer_count=4):
    super().__init__()
    self.batch_size = batch_size
    self.learning_rate = learning_rate
    layers = []
    for i in range(layer_count-1):
      layers.append((f"linear-{i}", nn.Linear(920, 920)))
      layers.append((f"relu-{i}", nn.ReLU()))
    layers.append((f"linear-{layer_count-1}", nn.Linear(920, 1)))
    self.seq = nn.Sequential(OrderedDict(layers))

  def forward(self, x):
    return self.seq(x)

  def training_step(self, batch, batch_idx):
    x, y = batch['binary'], batch['eval']
    y_hat = self(x)
    loss = F.l1_loss(y_hat, y)
    self.log("train_loss", loss)
    return loss

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

  def train_dataloader(self):
    dataset = EvaluationDataset(count=LABEL_COUNT)
    return DataLoader(dataset, batch_size=self.batch_size, num_workers=12, pin_memory=True)

LABEL_COUNT = 37164639
configs = [
           {"layer_count": 4, "batch_size": 512},
          #  {"layer_count": 6, "batch_size": 1024},
           ]
db.connect()
model = EvaluationModel.load_from_checkpoint("lightning_logs/version_47/checkpoints/modelV1")
model.eval()
bin=fen2BB.fen2BB("2r1k2r/pp1bppb1/2np1np1/q6p/3NP3/2N1BP1P/PPPQB1P1/1K1R3R b k - 3 12")
t =torch.from_numpy(bin)
device = torch.device('cpu')
model.to(device)
prediction = model(t)
print(prediction.item())
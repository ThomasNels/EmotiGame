from torch.utils.data import Dataset

class CreateDataset(Dataset):
    def __init__(self, features, labels, length):
        self.features = features
        self.labels = labels
        self.length = length

    def __getitem__(self, index):
        X = self.features[index:index + self.length]
        y = self.labels[index + self.length - 1]

        return X, y

    def __len__(self):
        return len(self.features) - self.length
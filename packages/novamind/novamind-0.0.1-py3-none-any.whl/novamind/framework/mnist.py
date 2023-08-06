class mnist:
    def __init__(self):
        self.train_images_in = open("G:\\MNIST\\MNIST_data\\train-images.idx3-ubyte", 'rb')
        self.train_labels_in = open("G:\\MNIST\\MNIST_data\\train-labels.idx1-ubyte", 'rb')
        self.test_images_in = open("G:\\MNIST\\MNIST_data\\t10k-images.idx3-ubyte", 'rb')
        self.test_labels_in = open("G:\\MNIST\\MNIST_data\\t10k-labels.idx1-ubyte", 'rb')
        self.batch_size = cfg.FLAGS.batch_size
        self.train_image = loadImageSet(self.train_images_in)  # [60000, 1, 784]
        self.train_labels = loadLabelSet(self.train_labels_in)  # [60000, 1]
        self.test_images = loadImageSet(self.test_images_in)  # [10000, 1, 784]
        self.test_labels = loadLabelSet(self.test_labels_in)  # [10000, 1]
        self.data = {"train": self.train_image, "test": self.test_images}
        self.label = {"train": self.train_labels, "test": self.test_labels}
        self.indexes = {"train": 0, "val": 0, "test": 0}

    def get_mini_batch(self, data_name="train"):
        if (self.indexes[data_name] + 1) * self.batch_size > self.data[data_name].shape[0]:
            self.indexes[data_name] = 0
        batch_data = self.data[data_name][
                     self.indexes[data_name] * self.batch_size:(self.indexes[data_name] + 1) * self.batch_size, :, :]
        batch_label = self.label[data_name][
                      self.indexes[data_name] * self.batch_size:(self.indexes[data_name] + 1) * self.batch_size, :]
        self.indexes[data_name] += 1
        y = np.zeros((self.batch_size, len(cfg.FLAGS.chars)))
        for kk in range(self.batch_size):
            y[kk, cfg.FLAGS.chars.index(str(int(batch_label[kk])))] = 1.0
        x = Batch_Normalization(batch_data)
        x = np.reshape(x, (16, 784, 1))
        x = np.reshape(x, (16, 28, 28, 1))
        return x, y

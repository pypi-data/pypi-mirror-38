from .dataset import dataset

__all__ = ['Database', 'connect']

def connect(url, **kwarg):

	return dataset.connect(url, **kwarg)
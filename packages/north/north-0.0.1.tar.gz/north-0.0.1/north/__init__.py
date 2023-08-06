# north namespace package should only contain the following line
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

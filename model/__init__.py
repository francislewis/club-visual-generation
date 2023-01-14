class Model:
    """
    Class for image generation ML models.
    Useful when devloping across platforms or versions (e.g. CPU only models vs GPU etc.) and to create model indepdent
    pipelines
    """

    def __init__(self, _valid_kwargs=tuple(), **kwargs):
        _valid_kwargs += ('model_name',)
        for k, v in kwargs.items():
            if k not in _valid_kwargs:
                raise ValueError("Keyword argument '{}' not supported".format(k))

        self.is_running = False

    def gen_txt2img(self, prompt):
        """
        prompt - string to be used as prompt for image generation
        """
        raise NotImplementedError

    def gen_img2img(self, image):
        """
        image - python object pointing to an image
        """
        raise NotImplementedError

from __init__ import Model


class film(Model):
    def __init__(self, imgarray, **kwargs):
        """
        data - 1D array of images

        This interpolates between generated image frames using the FILM interpolator
        """
        self.imgarray = imgarray
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('imgarray',)
        super().__init__(**kwargs)

    def generate(self):
        self.imgarray
        pass




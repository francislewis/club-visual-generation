from . import Model

class SD_CPU_V1_1(Model):
    def __init__(self, **kwargs):
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('num_inference_steps', )
        super().__init__(**kwargs)

    def gen_txt2img(self, height=512, width=768, prompt):
        """
        prompt - string to be used as prompt for image generation
        """
        raise NotImplementedError



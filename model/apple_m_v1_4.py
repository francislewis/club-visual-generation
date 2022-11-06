import torch
from diffusers import StableDiffusionPipeline
from __init__ import Model

class APPLE_M_V1_4(Model):
    def __init__(self, height=512, width=768, **kwargs):
        """
        steps - Number of inference steps, lower is worse quality but faster
        TODO: should this move to gen() in order to adjust quality depending on output speed?
        """
        self.height = height
        self.width = width
        self.run_num = 0
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('steps',)
        super().__init__(**kwargs)
        self.steps = kwargs.pop('steps','')


    def gen_txt2img(self, prompt):
        """
        prompt - string to be used as prompt for image generation
        """
        if self.run_num == 0:
            pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", height=self.height, width=self.width, num_inference_steps=1)
            pipe = pipe.to("mps")
            first_run = pipe(prompt).images[0]
            print("Setup Run")

        pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", height=self.height, width=self.width, num_inference_steps=self.steps)
        pipe = pipe.to("mps")
        image = pipe(prompt).images[0]
        self.run_num +=1
        return image


# ############ Example ############
# M_img2img_test_object = APPLE_M_V1_4()
# print(M_img2img_test_object.gen_txt2img(prompt="Horse riding on an astronaut"))

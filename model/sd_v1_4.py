import torch
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline
from model import Model
from PIL import Image


class sd_v1_4(Model):
    def __init__(self, height=512, width=768, **kwargs):
        """
        Inputs:
            steps - Number of inference steps, lower is worse quality but faster
                TODO: should this move to gen() in order to adjust quality depending on output speed?
            platform - ['SLOW', 'CUDA', 'MPS', 'CoreML']
            nsfw_filter - Boolean, default False
        """
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('steps', 'platform', 'nsfw_filter', )
        super().__init__(**kwargs)

        # Set internal variables
        self.height = height
        self.width = width
        self.steps = kwargs.pop('steps', '30')
        self.platform = kwargs.pop('platform', 'SLOW')
        self.run_num = 0
        self.nsfw_filter = kwargs.pop('nsfw_filter', False)


    def gen_txt2img(self, prompt):
        """
        prompt - string to be used as prompt for image generation
        """
        self.prompt = prompt

        # Setup pipeline
        if self.platform == 'SLOW':
            raise NotImplementedError

        elif self.platform == 'CUDA':
            # Note: revision="fp16" uses less VRAM
            self.pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", revision="fp16",
                                                       torch_dtype=torch.float16, height=self.height, width=self.width, num_inference_steps=self.steps)to("cuda")

        elif self.platform == 'MPS':
            # There is apparently a problem with MPS on Apple Silicon causing the first inference to be very slow
            # This attempts to get around it by running a quick 1-step inference if it's the first run then runs again
            if self.run_num == 0:
                print("Setup Run Starting")
                self.pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", height=self.height,
                                                               width=self.width, num_inference_steps=1).to("mps")
                self.pipe.enable_attention_slicing()
                self.pipe(self.prompt)
                self.run_num +=1
                print("Setup Run Finished")
                print("Running inference:")

                # Call the model again with same inputs
                self.__init__(height = self.height, width = self.width, steps = self.steps, platform = self.platform)

            else:
                self.pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", height=self.height,
                                                               width=self.width, num_inference_steps=self.steps).to("mps")
                self.pipe.enable_attention_slicing()

        elif self.platform == 'CoreML':
            raise NotImplementedError

        else:
            print(str(self.platform) + " is not a valid platform. Please try again with 'SLOW','CUDA' or 'MPS'")


        # Toggle NSFW filter
        if not self.nsfw_filter:
            def safety_checker(images, clip_input):
                return images, False
            self.pipe.safety_checker = safety_checker

        # Run Inference
        self.image = self.pipe(self.prompt).images[0] # Run inference
        self.run_num += 1  # Increment run number
        return self.image

    def gen_img2img(self, prompt, image, strength = 5):
        """
        img 2 img
        """

        # Setup Pipeline
        if self.platform == 'SLOW':
            raise NotImplementedError

        elif self.platform == 'CUDA':
            raise NotImplementedError

        elif self.platform == 'MPS':
            self.pipe_img2img = StableDiffusionImg2ImgPipeline().from_pretrained("./stable-diffusion-v1-4", height=self.height,
                                                               width=self.width, num_inference_steps=self.steps).to("mps")

            self.pipe_img2img(prompt=prompt, image=image, strength = strength)
            raise NotImplementedError

        elif self.platform == 'CoreML':
            raise NotImplementedError


    def save(self, image, filename):
        """
        Save the image outputted by a model (a PIL.Image.Image) to given filename
        """
        image.save(str(filename))

# ############ Example ############
# sd_test_object = sd_v1_4()
# sd_test_object.gen_txt2img(prompt="Horse riding on an astronaut")

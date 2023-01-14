import random
import threading
import time
from queue import Queue


class AbstractPipeline:
    def __init__(self, model):
        """
        Inputs:
            model: instance of model object that has already been initialised with setup arguments
        """

        # Set internal variables
        self.model = model  # model instance
        self.counter = 0  # Counting the number of times the model has been called, used to create directory to save each output
        self.input_queue = Queue()  # Initialise the Queue object

    def prompt_to_list(self, prompt, max_prompt_num=50):
        """
        Converts a prompt into a list of prompts to run through the model, removing random elements at equal intervals
        returns a list of these new prompts
        """
        self.orig_prompt = prompt  # Inputted prompt
        self.max_prompt_num = max_prompt_num  # Max number of iterations, will likely be less than this for equal splits

        init_split = self.orig_prompt.split()  # Split prompt into individual words
        len_split = len(init_split)  # Length of the original prompt is needed later, but we pop from the input to save memory (lol - compared to model VRAM) so need to set value here
        iterations = (self.max_prompt_num // len_split) * len_split  # True number of iterations
        prompt_list = []  # Where the final prompts to be run are saved

        # Randomly remove one word from the prompt in even iterations
        for i in range(iterations):
            if i != 0:
                if i % (iterations / len_split) == 0:
                    if len(init_split) > 1:
                        init_split.pop(random.randrange(len(init_split)))
                prompt = ' '.join(init_split)
                prompt_list.append(prompt)
        return prompt_list  # List of the prompts to run through the model

    def __queue_input(self):
        """
        Private method only to be used by AbstractPipeline object
        Take user input and add to queue, needs to be called on a separate thread
        """

        # Take prompt inputs while thread is running
        # TODO: could add a keyword like 'quit' to exit all processes
        while True:
            # Get input from the user
            input_str = input("Enter a value to add to the queue: ")

            # Add the input to the queue
            self.input_queue.put(input_str)

            # Print confirmation
            print("Prompt added to queue")

    def prompt_queue(self):
        self.input_thread = threading.Thread(target=self.__queue_input)
        self.input_thread.start()
        # Need to figure out how the queue works

    def processing(self):
        """
        This is the main loop which actually calls the generation model
        This is started/called on its own thread by self.processing_queue(), which itself is started by self.run()
        Potentially this is overly complex and could be simplified
        """
        while True:
            # TODO: check if model running and if not then initialise with queue item (I think this is done but needs more testing)
            if self.input_queue.qsize() > 0:
                if not self.model.is_running:
                    self.counter += 1  # Keep track of times self.processing has been called, used for directory name of output
                    # Check if the model is currently running and print (for TESTING)
                    print("Model running:" +str(self.model.is_running))
                    prompt_list = self.prompt_to_list(self.input_queue.get(),
                                                      max_prompt_num=4)  # TODO: set this max prompt number elsewhere
                    # TODO: need to iterate over this sub_directory as otherwise it overwrites last call
                    # TODO: want to be able to set this model method as an argument, so we can do different generation pipelines
                    self.model.gen_txt2vid(prompts=prompt_list, sub_directory=str(self.counter))

            # Only check every 5 seconds to not use too many CPU cycles
            time.sleep(5)

    def processing_queue(self):
        """
        This creates a thread for processing prompts through the model by starting self.processing() on a new thread
        The actual queue part is done within the self.processing() call as the target method called by threading.Thread can't have arguments
        """
        self.processing_thread = threading.Thread(target=self.processing)
        self.processing_thread.start()

    def run(self):
        """
        This method is called to start threads for both the prompt queue and the generation/processing queue
        """
        # Start a thread for prompts
        self.prompt_queue()
        # Start a thread for processing/generating prompts through the model
        self.processing_queue()


# Test/Example
from model.sd_videos import sd_videos

# Setup model to be used
test_model = sd_videos(steps=3, output_dir='test_vid', interpolation_steps=1, platform='SLOW')

# Setup abstract pipeline
test_pipeline = AbstractPipeline(test_model)

# Run pipeline
test_pipeline.run()

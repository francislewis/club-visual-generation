# club-visual-generation

Software to generate interactive visuals in a club-night enviroment

Currently all of the ML is done with [Stable Diffusion](https://github.com/CompVis/stable-diffusion).

### Plan / To-Do
- Create model object with CPU-only, CUDA and img2img options
- Find a way to abstract the images at a similiar rate
  -  Maybe img2img without current 'prompt hacking'
- Allow option for image or text input
- Integrate Rekordbox code for music sync and think about output methods 
- Control quality/speed trade off for a fixed generation time 

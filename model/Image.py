import pygame
from PIL import Image as PILImage

class Image:
    class AnimatedImage:
        def __init__(self, frames, fps=30):
            self.frames = [frame.convert_alpha() for frame in frames]  # Ensure all frames have alpha
            self.frame_count = len(frames)
            self._current_frame = 0
            self.fps = fps
            self.last_update = pygame.time.get_ticks()
            self.frame_duration = 1000 // fps  # Milliseconds per frame

        @property
        def current_frame(self):
            now = pygame.time.get_ticks()
            elapsed = now - self.last_update
            if elapsed >= self.frame_duration:
                frames_to_advance = elapsed // self.frame_duration
                self._current_frame = (self._current_frame + frames_to_advance) % self.frame_count
                self.last_update += frames_to_advance * self.frame_duration
            return self.frames[self._current_frame]

    peaShooter = None
    wallnute = None
    zoombie = None
    pea = None
    sunflower = None

    @staticmethod
    def load_images():
        def load_gif_frames(file_path, size):
            gif = PILImage.open(file_path)
            frames = []
            try:
                while True:
                    frame = pygame.image.fromstring(
                        gif.tobytes(), gif.size, gif.mode
                    )
                    frame = pygame.transform.scale(frame, size)
                    frames.append(frame)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            return frames

        Image.peaShooter = Image.AnimatedImage(load_gif_frames("assets/peashooter/peashooter.gif", (80, 120)))
        Image.zoombie = Image.AnimatedImage(load_gif_frames("assets/zombie/zombie_walk.gif", (80, 120)))
        Image.zoombieEat = Image.AnimatedImage(load_gif_frames("assets/zombie/zombie_eat.gif", (80, 120)))
        Image.zoombieDie = Image.AnimatedImage(load_gif_frames("assets/zombie/zombie_die.gif", (80, 120)))
        Image.sunflower = Image.AnimatedImage(load_gif_frames("assets/sunflower/sunflower2.gif", (80, 120)))
        Image.wallnute = pygame.transform.scale(
            pygame.image.load("assets/models/wallNut.png").convert_alpha(), (80, 120)
        )
        Image.pea = pygame.transform.scale(
            pygame.image.load("assets/images/pea.webp").convert_alpha(), (50, 50)
        )
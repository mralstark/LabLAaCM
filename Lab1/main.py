import tkinter as tk
import math
from mathdevs import helix, generate
from graphics import GfxEngine


class HelixViewer:
    

    def __init__(self, root):
        self.root = root
        self.root.title("3D Винтовая Поверхность")
        self.root.geometry("800x650")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.engine = GfxEngine()

        self.params = {"alpha": 0.5, "beta": 0.5, "zlim": 0.5}
        self.u_range = (0, 4 * math.pi)
        self.v_range = (-2, 2)

        self.create_controls()

        self.redraw()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def create_controls(self):
        
        frame = tk.Frame(self.root)
        frame.pack(padx=5, pady=5, fill=tk.X)

        tk.Label(frame, text="α:").grid(row=0, column=0)
        self.alpha_s = tk.Scale(
            frame, from_=0.01, to=1, resolution=0.05,
            orient=tk.HORIZONTAL, command=lambda v: self.set_param("alpha", v))
        self.alpha_s.set(self.params["alpha"])
        self.alpha_s.grid(row=0, column=1)

        tk.Label(frame, text="β:").grid(row=0, column=2)
        self.beta_s = tk.Scale(
            frame, from_=0.01, to=1, resolution=0.05,
            orient=tk.HORIZONTAL, command=lambda v: self.set_param("beta", v))
        self.beta_s.set(self.params["beta"])
        self.beta_s.grid(row=0, column=3)

        tk.Label(frame, text="Z-лимит:").grid(row=0, column=4)
        self.zlim_s = tk.Scale(
            frame, from_=0.2, to=1, resolution=0.05,
            orient=tk.HORIZONTAL, command=lambda v: self.set_param("zlim", v))
        self.zlim_s.set(self.params["zlim"])
        self.zlim_s.grid(row=0, column=5)

        self.wireframe = tk.BooleanVar()
        tk.Checkbutton(frame, text="Каркас", variable=self.wireframe, command=self.redraw).grid(row=0, column=6)

        tk.Button(frame, text="Сброс", command=self.reset_view).grid(row=0, column=7)

    def set_param(self, key, value):
       
        self.params[key] = float(value)
        self.redraw()

    def reset_view(self):
       
        self.engine.rot_x = self.engine.rot_y = self.engine.rot_z = 0
        self.redraw()

    def on_click(self, e):
        
        self.last_x, self.last_y = e.x, e.y

    def on_drag(self, e):
    
        dx = e.x - self.last_x
        dy = e.y - self.last_y
        self.last_x, self.last_y = e.x, e.y

        self.engine.rot_y += dx * 0.01
        self.engine.rot_x -= dy * 0.01
        self.redraw()

    def redraw(self):
        
        self.canvas.delete("all")

        points = generate(helix, self.u_range, self.v_range,
                          u_steps=50, v_steps=30, **self.params)

        self.engine.draw_surf(
            self.canvas, points,
            color="#BDB76B",
            wireframe=self.wireframe.get()
        )

        self.engine.draw_axes(self.canvas)

        self.canvas.create_text(10, 10, anchor="nw",
                                text="Винтовая поверхность",
                                font=("Arial", 12, "bold"), fill="black")


if __name__ == "__main__":
    import sys
    import os

    
    sys.path.append(os.path.dirname(__file__))

    root = tk.Tk()
    app = HelixViewer(root)
    root.mainloop()
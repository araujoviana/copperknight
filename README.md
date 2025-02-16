# copperknight

> THIS IS AN OLD PROJECT FOR [CS50W](https://cs50.harvard.edu/web/2020/)

## Installation and usage

``` bash
git clone https://github.com/araujoviana/copperknight
cd copperknight

python manage.py runserver
```

## Distinctiveness and Complexity

### The Concept

copperknight is a drawing website that provides a customizable canvas with various tools for drawing. While it may not have the most complex drawing software tools, it is very beginner-friendly. Additionally, since the artwork is stored on the server, you can access it from anywhere, even on your phone. Another advantage is that the images are saved in base64 format, making it easier to share them online on other platforms. If you're confident enough, you can also upload your artwork to the Showcase for others to see, potentially adding it to their "favorited" tab or even following you.

### The Canvas

The main purpose behind this project is the canvas itself. I wanted to create a website where users could draw and scribble directly from their browser without the need to download any software. However, it's important to remember that this website is more suitable for casual drawings rather than professional ones, like those created using Photoshop or Krita.

Before starting this project, I wasn't aware of the `<canvas>` element, so I initially thought it would be much more complex than it actually was. Fortunately, I didn't have to reinvent the wheel, as the canvas element provided (some of) the tools that I needed.

While the website primarily focuses on drawing, it also allows users to store and share imported images. So, if you prefer to create your images using other tools, you can simply import them onto the website.

Surprisingly, importing to mobile devices was not as challenging as I thought. Which highlights the importance of the website, because there aren't many drawing apps or websites that offer both drawing capabilities and the ability to easily share the created artwork.

Implementing each tool was its own challenge, even the most simple ones like the "Draw a circle" tool took a lot time to get to work, but among others the fill tool was one of the hardest to implement, and it works perfectly (well as perfect as the bucket tool on MS Paint does), but the hardest one was probably the Record tool (and even after a ton of testing it still has some problems, but i believe that they're minor enough that it wouldn't bother any actual user), i know there is a `save` and `restore` feature on `<canvas>` but it just **wouldn't** work, so i decided to just record movement while the user was drawing, which also affects the fill tool, but since the colors used are saved it isn't that hard to redo fills.

Saving the images in Base64 format was initially an accidental discovery that turned into a feature. I initially encountered some issues with saving the images in the models, which led me to learn about Base64 and how it can store entire images as text. Consequently, I implemented a `TextField()` model to achieve this functionality.

### The Showcase

I intentionally avoided making the website feel too much like a social media platform for a couple of reasons:

1. Network problem set.
2. Adding excessive social media features would take away from the beginner-friendly charm of the website.
3. The main focus of the project is the canvas.

Instead of adding likes and comments, I opted for a favorite and following tab. I also preferred to not create a "popular" or "most liked" tab because i felt like it was a good idea not to separate popular artists from beginners.

## Whats Included
### Static
The static folder contains the favicon, the logo (both of which contain the same picture) and the CSS that has the (most) stylings and animations.

### Models
This project only contains 3 models: ``User``, which contains the emails, passwords, usernames, and followers; ``Opus``, which contains the Base64 text of the images, their title, if they're private, when they were created, and who made them; and ``FavoritedOpus``, which contains the users who favorited a picture and which picture it was.
### Templates
- `layout.html` contains the Navbar and the `<head>` of the project. There is no `login.html` because that's handled in the dropdown menu in the navbar, but creating a new account goes to `register.html`. Other HTMLs are blocks loaded on `layout.html`.
- `index.html` contains the home page, which shows the most recent picture submitted, and two links: one for drawing (if the user is logged in) and another that goes to the Showcase.
- `draw.html` is the main file of the whole project and contains the HTML for the canvas and its tools, and also the JavaScript for making it work. Adding new features probably won't break the code, but if it does, the canvas will simply stop working completely.
- `showcase.html` loads the model Opus in reverse chronological order and checks if they're public. If so, it displays them in order. Users can double-click to add pictures to their favorited tab.


Other HTMLs are slight variations of `showcase.html`:
1. `favorited.html` - contains all the user-favorited pictures
2. `following.html` - contains posts by followed users
3. `gallery.html` - contains the user's art, even the private ones
4. `search.html` - shows pictures with a title similar to the search query
5. `profile.html` - shows public art by a specific user

### Views and Admin
`views.py` contains most of the logic behind submitting images, following, favoriting, and others. The paginator is set to 10, but it can be easily changed with `PAGIVALUE`. `admin.py` lets a superuser view and edit the information contained in each model.

## How to use copperknight

### Disclaimer

Please note that the project includes two pictures in the gallery. These pictures are essential for the proper functioning of the project and should not be removed or deleted. Removing these pictures may result in errors or broken functionality within the application. If you decide to delete these pictures, please ensure that there are at least two pictures remaining in the `Opus` model.

### Third-party libraries
There are no third-party Python libraries necessary for running the code. Migrating the models and executing `python manage.py runserver` should be enough to start copperknight.

### How to start drawing
To start drawing, the user needs to create an account. After that, they are able to create their drawing using the canvas (click on "Draw" in the navbar to go to the canvas).

Drawing on the canvas is pretty simple. Just click (or touch) and drag around to draw.

### Tools and their functions:
File Section
- Import Image: Lets the user select an image file and imports it to the canvas.
- Change Resolution: Shows a form where the user can choose the width and height of the image. **Changing the resolution will clean the canvas, so do this first before drawing anything important**.
- Full Clear: Clears the canvas completely, good for making drawings with transparent backgrounds.
- White Fill & Save as PNG: Self-explanatory. Fills the canvas with white and saves the image as a PNG file.
- Upload and Save to Gallery: Encodes the image to Base64 and uploads it to the Gallery. If the Private checkbox is checked, then the image won't be uploaded to the Showcase and will only be viewable in the Gallery.

Drawing tools

- Eraser: Toggles the eraser on and off.
- Brush Color: Prompts the user to insert the hex code of a color. The color inserted becomes the brush color and is saved. The maximum number of custom colors that can be stored is 10.
- Color Presets: Dropup containing various preset colors.
- Fill: Works like the bucket tool on MS Paint. Fills a non-transparent area with the user's current brush color. Toggles off each time it's used.
- Draw: Used for drawing shapes. Click and drag to draw a shape. However, it's important to note:
  1. The square shape may not correspond with your mouse position.
  2. Clicking and dragging changes the radius of the circle, not the full diameter.

- Brush Size: Changes the brush size, defaulted to 1.

Other tools
- Record:
  1. Paste to Canvas: Pastes what was recorded onto the canvas. It won't paste fills nor shapes, but it will connect separate drawings together.
  2. Start & Stop: Toggles the recording on and off.
  3. Reset Recording: Resets what was recorded.

- Add Gradient: Prompts the user (with an alert) with two colors, one for the start of the gradient and the other for the end. It will fill the canvas with the gradient, so use this before drawing.
- Copy Base64: Copies the Base64 of the current drawing on the canvas to the clipboard without saving. Note that it might not work with HD imported images, but it depends a lot.

### Checking out other people's drawings
On the Showcase tab, it's possible to see other people's artwork and add them to Favorited by double-clicking on the picture. By clicking on someone's name, you can see their art and even follow them to add them to your Following tab.

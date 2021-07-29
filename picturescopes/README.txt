convert IMG_0169.jpg -resize 450x620 -quality 100 IMG_0169_resize.jpg
montage -mode concatenate -tile 2x3 *resize.jpg -geometry +10+10 out.jpg
convert out.jpg -resize 1080x1920 -background black -gravity center -extent 1080x1920 out1.jpg

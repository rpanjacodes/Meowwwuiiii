const fs = require("fs");
const path = require("path");

const imagesDir = path.join(__dirname, "images");
let currentIndex = 0;

function getNextImage() {
    const images = fs.readdirSync(imagesDir).filter(file => /\.(jpg|png)$/i.test(file));
    if (images.length === 0) return null;

    const imagePath = path.join(imagesDir, images[currentIndex]);
    currentIndex = (currentIndex + 1) % images.length;
    
    return imagePath;
}

module.exports = { getNextImage };

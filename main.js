const { fetchNextSong } = require("./youtubeHandler");
const { getNextImage } = require("./imageRotator");
const ffmpeg = require("fluent-ffmpeg");
const config = require("./.config/config.json");

async function startStreaming() {
    console.log("Starting 24/7 YouTube livestream...");

    while (true) {
        const songUrl = await fetchNextSong();
        if (!songUrl) continue;

        const backgroundImage = getNextImage();
        if (!backgroundImage) {
            console.error("No background images found!");
            break;
        }

        ffmpeg()
            .input(backgroundImage)
            .input(songUrl)
            .complexFilter([
                "[0:v]scale=1280:720[bg];",
                "[1:a]volume=1.0[audio]"
            ])
            .map("[bg]")
            .map("[audio]")
            .videoCodec("libx264")
            .audioCodec("aac")
            .format("flv")
            .output(config.streamUrl)
            .on("start", () => console.log("Streaming started!"))
            .on("error", err => console.error("FFmpeg error:", err))
            .run();

        await new Promise(resolve => setTimeout(resolve, config.imageRotationInterval * 1000));
    }
}

startStreaming();

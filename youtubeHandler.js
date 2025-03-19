const youtubedl = require("youtube-dl-exec");
const fs = require("fs-extra");
const path = require("path");
const config = require("./.config/config.json");

async function fetchNextSong() {
    try {
        const output = await youtubedl(config.playlistUrl, {
            dumpSingleJson: true
        });

        const videos = output.entries || output.items;
        if (!videos || videos.length === 0) throw new Error("No videos found!");

        const video = videos[Math.floor(Math.random() * videos.length)];
        return video.url;
    } catch (err) {
        console.error("Error fetching song:", err);
        return null;
    }
}

module.exports = { fetchNextSong };

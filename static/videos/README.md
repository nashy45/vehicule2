# Video Upload Instructions

## How to Add Your Showroom Video

1. **Prepare Your Video**:
   - Format: MP4 (recommended) or WebM
   - Resolution: 1920x1080 (Full HD) or 1280x720 (HD)
   - Duration: 1-3 minutes recommended
   - File size: Under 50MB for best loading performance

2. **Name Your Video**:
   - Rename your video file to: `showroom.mp4`
   - Or: `showroom.webm`

3. **Upload to This Folder**:
   - Copy your video file to this folder: `static/videos/`
   - Replace any existing showroom video

4. **Update the Thumbnail (Optional)**:
   - The video thumbnail is at: `static/images/video-thumbnail.png`
   - You can replace it with a frame from your video
   - Recommended size: 1280x720 pixels

## Video Optimization Tips

### Reduce File Size:
Use a video converter tool like HandBrake (free):
- Format: MP4 (H.264)
- Quality: RF 23-25 (good balance of quality and size)
- Framerate: 30 FPS
- Audio: AAC, 128 kbps

### Online Converters:
- CloudConvert.com
- Online-Convert.com
- Convertio.co

### Recommended Video Content:
- Showroom tour
- Vehicle showcase
- Customer testimonials
- Company introduction
- Behind-the-scenes of vehicle inspection

## Troubleshooting

**Video Not Playing?**
- Check file name is exactly: `showroom.mp4` or `showroom.webm`
- Verify video is in `static/videos/` folder
- Clear browser cache and refresh page
- Try converting to MP4 format

**Video Loading Slow?**
- Compress video to reduce file size
- Use MP4 format with H.264 codec
- Consider hosting on YouTube/Vimeo for large files

**Alternative: YouTube/Vimeo Embed**
If you prefer to host on YouTube or Vimeo:
1. Upload video to YouTube/Vimeo
2. Get the embed code
3. Edit `templates/index.html`
4. Replace the `<video>` tag with the embed code

Example YouTube embed:
```html
<div class="ratio ratio-16x9">
    <iframe src="https://www.youtube.com/embed/YOUR_VIDEO_ID" 
            allowfullscreen></iframe>
</div>
```

## Current Setup

The homepage displays:
- Video thumbnail from: `static/images/video-thumbnail.png`
- Video file from: `static/videos/showroom.mp4`
- Play button overlay
- When clicked, video plays in place of thumbnail

Once you add your video file named `showroom.mp4` to this folder, it will automatically appear on the homepage!

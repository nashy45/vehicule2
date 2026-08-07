# Media Guide: Images and Videos

## ✅ Images Already Added

I've organized your images and added them to the website:

### 1. Hero Section Image
- **File**: `static/images/hero-car.jpg` (your Mercedes image)
- **Location**: Homepage hero section (large background image)
- **Size**: Full width, automatically responsive
- **Purpose**: Main eye-catching image when visitors land on your site

### 2. Showroom/Gallery Image  
- **File**: `static/images/showroom.jpg`
- **Location**: Homepage gallery section
- **Size**: 50% width in two-column layout
- **Purpose**: Showcase your showroom/dealership

### 3. Video Thumbnail
- **File**: `static/images/video-thumbnail.png`
- **Location**: Homepage video section
- **Size**: Full width of video player
- **Purpose**: Preview image before video plays

## 📁 Where Your Media Files Are Located

```
static/
├── images/
│   ├── hero-car.jpg          ✅ Mercedes - Homepage hero
│   ├── showroom.jpg          ✅ Your showroom - Gallery section  
│   ├── video-thumbnail.png   ✅ Video preview - Video section
│   └── uploads/              📁 Vehicle photos (from admin panel)
│
└── videos/
    ├── README.md             📄 Instructions for adding videos
    └── showroom.mp4          ⚠️ ADD YOUR VIDEO HERE
```

## 🎬 Adding Your Video

### Step 1: Prepare Your Video
1. Choose your best showroom or vehicle showcase video
2. **Recommended specs**:
   - Format: MP4
   - Resolution: 1920x1080 or 1280x720
   - Duration: 1-3 minutes
   - File size: Under 50MB

### Step 2: Name and Upload
1. Rename your video to: **`showroom.mp4`**
2. Copy it to: `static/videos/showroom.mp4`
3. Refresh your website - video will work automatically!

### Alternative: Use YouTube
If your video is on YouTube:
1. Upload to YouTube
2. Open `templates/index.html`
3. Find the `<video>` tag (search for "showroomVideo")
4. Replace with YouTube embed code

## 🖼️ Adding More Images

### Homepage Gallery
To add more gallery images:
1. Add images to `static/images/`
2. Edit `templates/index.html`
3. Add new gallery items in the "Image Gallery Section"

Example:
```html
<div class="col-md-4">
    <div class="gallery-item position-relative overflow-hidden rounded shadow-lg">
        <img src="{{ url_for('static', filename='images/your-new-image.jpg') }}" 
             alt="Description" 
             class="img-fluid w-100 gallery-img">
        <div class="gallery-overlay">
            <h4>Title</h4>
            <p>Description</p>
        </div>
    </div>
</div>
```

### Vehicle Photos (Admin Panel)
1. Login to admin panel
2. Go to "Add Vehicle" or "Edit Vehicle"
3. Use the image upload field
4. Images automatically saved to `static/images/uploads/`

## 🎨 Image Optimization Tips

### Recommended Sizes:
- **Hero image**: 1920x1080px (landscape)
- **Gallery images**: 1200x800px
- **Vehicle photos**: 800x600px
- **Thumbnails**: 400x300px

### Optimization Tools (Free):
- **TinyPNG.com** - Compress without losing quality
- **Squoosh.app** - Google's image optimizer
- **ImageOptim** - Desktop app for Mac
- **RIOT** - Desktop app for Windows

### File Formats:
- **JPG**: Best for photos (vehicles, showroom)
- **PNG**: Best for logos, graphics with transparency
- **WebP**: Modern format, smaller file size

## 🚀 What's Working Now

### ✅ Homepage Features:
1. **Hero Section**: Full-width Mercedes image with text overlay
2. **Features**: Three icon boxes (Quality, Prices, Support)
3. **Video Section**: Thumbnail with play button (needs video file)
4. **Stats**: Four statistics boxes (Vehicles, Clients, Rating, Experience)
5. **Gallery**: Two large images side-by-side
6. **Featured Vehicles**: Shows featured vehicles from database
7. **Call to Action**: Buttons to inventory and contact

### 🎯 Interactive Elements:
- Hover effects on gallery images (zoom in)
- Play button for video
- Responsive design (mobile-friendly)
- Smooth animations

## 📱 Mobile Optimization

All images are automatically responsive:
- Hero section adjusts height on mobile
- Gallery stacks vertically on small screens
- Video player adapts to screen size
- Images load efficiently

## 🔧 Troubleshooting

### Images Not Showing?
1. Check file path is correct
2. Clear browser cache (Ctrl+F5)
3. Verify image is in `static/images/` folder
4. Check image file extension matches code (.jpg vs .jpeg)

### Images Loading Slowly?
1. Compress images using TinyPNG or similar
2. Reduce image dimensions before uploading
3. Convert to WebP format for smaller file size

### Video Not Playing?
1. Ensure file is named exactly: `showroom.mp4`
2. Check it's in `static/videos/` folder
3. Try different video format (MP4, WebM)
4. Consider YouTube embed for large files

## 📞 Need Help?

If you need to:
- Change image positions
- Add more gallery sections
- Customize layouts
- Add image carousels
- Create photo galleries

Just let me know and I'll help customize it further!

## 🎉 Next Steps

1. ✅ Images are already integrated
2. ⚠️ Add your video file (`showroom.mp4`)
3. ✅ Test on different devices
4. ✅ Add more vehicle photos through admin panel
5. ✅ Customize text and descriptions as needed

Your website now has beautiful, professional imagery! Add your video and you're all set! 🚗✨

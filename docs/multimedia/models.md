# Models

## Video
The video models keeps track of the video uploaded to the website. 
### Fields
```
{
  title   : title keeps the title of the video, 
  file    : file refers to the file keeping the video. 
  date    : date refers to the date the video is created or uploaded
}
```

## Image
The image model keeps track of the image uploaded to the website. 
### Fields
```
{
  title   : title keeps the title of the image
  file    : file refers to the file keeping the image. 
  alt     : alt keeps the alternate for the image. 
  date    : date keeps track of the date the image is created or uploaded
}
```

## Multimedia
The multimedia model connects Images and Videos together, forming a post. It contains the following fields : 
```
{
  title   : keeps the title fo the multimedia post, 
  slug    : keeps the slug of the multimedia, 
  tags    : is a many to many field connecting multimedia with tags model for filtering, 
  images  : many to many field connecting image to multimedia, 
  videos  : many to many field connecting videos to multimedia, 
  date    : the date field contains the date the post is created
  previews: show the preview image for the multimedia post. 
}
```
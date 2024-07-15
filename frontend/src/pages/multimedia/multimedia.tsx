import Lister from "../../components/lister";
import React, { lazy, useState } from "react";
import Card from '@mui/material/Card';
import { Box, Button, ButtonBase, CardActionArea, CardHeader, CardMedia, Dialog, DialogContent, DialogTitle, Divider, Grid, Icon, ImageList, ImageListItem, ImageListItemBar, Paper, Stack, Typography, useTheme } from "@mui/material";

import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, EffectFade, Keyboard, Navigation, Pagination, Zoom } from 'swiper/modules';
import "../../components/css/multimedia.css"
import { fakeMultimediaData, MultimediaImageT, MultimediaT } from "../../API/multimedia";

import 'swiper/css';
import 'swiper/css/zoom';
import 'swiper/css/effect-fade';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { HighlightedLetter } from "../../core/components";
import { redirect, useNavigate, useParams } from "react-router-dom";

// const fakeCarouselData = ["facebook-logo.png", "kisaLogo.png", "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"]
// const fakeImageData = [""]
// const styles = {
//     card: {
//         margin: '15px 10px',
//         padding: 0,
//         borderRadius: '16px',
//         backgroundColor: 'lightskyblue'
//     },
//     small: {
//         gridRowEnd: 'span 26'
//     },
//     medium: {
//         gridRowEnd: 'span 33'
//     },
//     large: {
//         gridRowEnd: 'span 45'
//     }
// }

// const CardRender = ({ data }: { data: string }) => {
//     const [hover, setHover] = useState(false);

//     const cardStyle = {
//         boxShadow: hover
//             ? 'rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px'
//             : '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
//         transition: 'transform 0.3s ease, box-shadow 0.3s ease',
//         transform: hover ? 'scale(1.05)' : 'scale(1)'
//     };

//     return (
//         <Card className="card" style={cardStyle}
//             onMouseEnter={() => setHover(true)}
//             onMouseLeave={() => setHover(false)}
//         >
//             <CardContent className="cardContent">
//                 <span className="date">date</span>
//                 <img src={data} />
//                 <span className="headline">HeadLine</span>
//             </CardContent>
//         </Card>
//     );
// }

// const CarouselRender = ({ data }: { data: string[] }) => {
//     const [currentIndex, setCurrentIndex] = useState(0);
//     return (
//         <div className="carouselContainer">
//             <center>
//                 <span className="bgText">OUR PROUDLY PRESENT</span>
//                 <div className="carousel">
//                     {data.map((image, index) => (
//                         <CardRender data={image} />
//                     ))}
//                 </div>
//                 <div>
//                     <br />
//                     <span className="dot" ></span>
//                     <span className="dot" ></span>
//                     <span className="dot" ></span>
//                     <br />
//                     <br />
//                 </div>
//             </center>
//         </div>
//     );
// }

// type CardProps = {
//     size: "small" | "medium" | "large";
// };

// function PinterestCard(props: CardProps) {
//     return (
//         <div style={{
//             ...styles.card,
//             ...styles[props.size]
//         }}>
//             <img src = "facebook-logo.png" width="10%" height="10%"/>
//         </div>
//     )
// }

// const PinterestRender = () => {
//     return (
//         <div className="pinterestContainer">
//             <PinterestCard size = "small"/>
//             <PinterestCard size = "medium"/>
//             <PinterestCard size = "large"/>
//             <PinterestCard size = "small"/>
//         </div>
//     )
// }

// const Multimedia = () => {
//     return (
//         <>
//             <center>
//                 <h2>Multimedia</h2>
//             </center>
//             <br />
//             <br />
//             <div className="carousel">
//                 <CarouselRender data={fakeCarouselData} />
//             </div>
//             <br />
//             <br />
//             <div>
//                 <PinterestRender />
//             </div>
//         </>
//     )
// }

function getRandomIntBetween(end: number, start: number=0) {
    const interval = end - start;
    return Math.floor(Math.random()*interval)+start;
}

type PreviewCardProps = {
    title: string;
    slug: string;
    image: MultimediaImageT;
}

const PreviewCard = ({ title, slug, image }: PreviewCardProps) => (
    <SwiperSlide>
        <Card>
            <CardActionArea
                href={"/multimedia/"+slug}
            >
            <CardHeader 
            title={title}
            subheader={new Date(image.date).toDateString()}
            titleTypographyProps={{variant: "h3"}}
            />
        </CardActionArea>
        <CardMedia 
            component="img"
            image={image.href}
            alt={image.alt}
            sx={{ height: "min(75vh, 75vw)", objectFit: "contain" }}
        />
        </Card>
    </SwiperSlide>
);

const getIntervalDateStampBetween = (x: Date, y:Date) => (x.getDate() === y.getDate())? x.toDateString(): x.toDateString() + "-" + y.toDateString();

const AlbumCover = ({ title, images, slug }: MultimediaT) => {
    const navigate = useNavigate();
    
    return (
        <Grid item xs={12} sm={6} md={4} lg={3}>
            <ButtonBase component={Paper} onClick={()=>{navigate("./"+slug)}} className="cover">
            <Box sx={{padding: "5% 0 5% 30px"}} width="100%" height="100%">
                <Stack paddingRight="5%" textAlign="right" sx={{backgroundColor: "primary.main"}}>
                <Typography variant="fancy_h4">{title}</Typography>
                <Typography>{
                    getIntervalDateStampBetween(new Date(images[0].date), new Date(images[images.length-1].date)) 
                }</Typography>
                </Stack>
            </Box>
            </ButtonBase>
        </Grid>
    );
}

const sortMultimediaImagesByDateTime = (imgs: MultimediaImageT[]) => imgs.sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
);

export const Multimedia = () => {
    const slug = useParams().slug as string;
    const index = fakeMultimediaData.findIndex(multimedia=>(multimedia.slug===slug));
    const [zoomedImageIndex, setZoomedImageIndex] = useState(0);
    const [zoomDialogState, setZoomDiaglogState] = useState(false);
    const aspectRatio = window.innerWidth / window.innerHeight;

    if (index === -1)
        redirect("/multimedia/");

    type ImageGroupedByDate = {
        date: Date;
        startIndex: number;
        images: MultimediaImageT[];
    };

    const groupsByDate = fakeMultimediaData[index].images.reduce(
        (accumulator: ImageGroupedByDate[], currentVal: MultimediaImageT, currentIndex: number) => {
            const currentValDate = new Date(currentVal.date);
            if (accumulator.length === 0 || accumulator[accumulator.length-1].date.toDateString() !== currentValDate.toDateString()) {
                accumulator.push({
                    date: currentValDate,
                    startIndex: currentIndex,
                    images: [currentVal],
                })
            } else {
                accumulator[accumulator.length-1].images.push(currentVal);
            }
            return accumulator;
        },
        []);

    const imageOnClickHandler: React.MouseEventHandler<HTMLLIElement> = (event) => {
        console.log(event.currentTarget);
        setZoomedImageIndex(parseInt(event.currentTarget.id));
        setZoomDiaglogState(true);
    }

    const ImageGroupByDate = ({date, startIndex, images}: ImageGroupedByDate) => (
        <Stack>
            <Typography variant="h3">{date.toDateString()}</Typography>
            <ImageList variant="masonry">
                {
                    images.map((img, index) => (
                        <ImageListItem key={startIndex+index} onClick={imageOnClickHandler}>
                            <img
                                src={img.href}
                                alt={img.alt}
                                loading="lazy"
                            />
                        </ImageListItem>
                    ))
                }
            </ImageList>
            <Divider/>
        </Stack>
    );

    return (
        <Stack>
            <Stack textAlign="center">
                <Typography variant="fancy_h1">{fakeMultimediaData[index].title}</Typography>
                <Typography>{fakeMultimediaData[index].description}</Typography>
            </Stack>
            <Divider/>
            {groupsByDate.map(ImageGroupByDate)}
            <Dialog open={zoomDialogState} onClose={()=>setZoomDiaglogState(false)} maxWidth="lg">
                <DialogTitle variant="fancy_h2" textAlign="center">
                    {fakeMultimediaData[index].title}
                </DialogTitle>
                <DialogContent>
                <Typography>
                    {fakeMultimediaData[index].description}
                </Typography>
                <Swiper
                    initialSlide={0}
                    spaceBetween={30}
                    effect={'fade'}
                    keyboard={{
                        enabled: true,
                    }}
                    navigation={true}
                    pagination={{
                        clickable: true,
                    }}
                    fadeEffect={{
                        crossFade: true
                    }}
                    zoom={true}
                    modules={[Zoom, EffectFade, Keyboard, Navigation, Pagination]}
                >
                    {fakeMultimediaData[index].images.map(img => (
                        <SwiperSlide>
                            <Stack className="swiper-zoom-container" sx={{aspectRatio: aspectRatio}}>
                            <Typography width="100%" textAlign="right">{new Date(img.date).toDateString()}</Typography>
                            <img
                                src={img.href}
                                alt={img.alt}
                                loading="lazy"
                                style={{objectFit: "contain", width: "100%" }}
                            />
                            </Stack>
                        </SwiperSlide>
                    ))}
                </Swiper>
                </DialogContent>
            </Dialog>
        </Stack>
    );
};

export const MultimediaHome = () => {
    return (
        <Stack gap={2}>
            <Stack>
                <Typography variant="fancy_h1" textAlign="center"><HighlightedLetter letter="Memories"/></Typography>
                <Typography variant="subtitle1" textAlign="center">Happy times come and go, but the memories stay forever...</Typography>
            </Stack>
            <Swiper
                autoplay={{
                    delay: 5000,
                }}
                spaceBetween={30}
                effect={'fade'}
                keyboard={{
                    enabled: true,
                }}
                navigation={true}
                pagination={{
                    clickable: true,
                }}
                fadeEffect={{
                    crossFade: true
                }}
                modules={[Autoplay, EffectFade, Keyboard, Navigation, Pagination]}
                className="w-5/6"
            >
                {fakeMultimediaData.map(multimedia => {
                    return {
                        title: multimedia.title,
                        slug: multimedia.slug,
                        image: multimedia.images[getRandomIntBetween(multimedia.images.length)]
                    }
                }).map(PreviewCard)}
            </Swiper>
            <Divider/>
            <Typography variant="h2" textAlign="center">Wayback Machine</Typography>
            <Divider/>
            <Grid container spacing={2}>
                {fakeMultimediaData.map(AlbumCover)}
            </Grid>
        </Stack>
    );
}


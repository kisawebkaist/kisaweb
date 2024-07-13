import Lister from "../../components/lister";
import React, { useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { CardActionArea, CardHeader, CardMedia, Divider, Stack, Typography } from "@mui/material";

import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, EffectFade, Keyboard, Navigation, Pagination } from 'swiper/modules';
import "../../components/css/multimedia.css"
import { fakeMultimediaData, MultimediaImageT, MultimediaT } from "../../API/multimedia";

import 'swiper/css';
import 'swiper/css/effect-fade';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { HighlightedLetter } from "../../core/components";

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
    description: string;
    image: MultimediaImageT;
}

const PreviewCard = ({ title, description, image }: PreviewCardProps) => (
    <SwiperSlide>
        <Card>
        <CardHeader 
            title={title}
            subheader={new Date(image.date).toDateString()}
            titleTypographyProps={{variant: "h3"}}
        />
            <CardActionArea
                href="/hello"
            >
            <CardMedia 
                component="img"
                image={image.href}
                alt={image.alt}
                sx={{ height: "min(75vh, 75vw)", objectFit: "contain" }}
            />
            </CardActionArea>
        <CardContent>
            <Typography>
                {description}
            </Typography>
        </CardContent>
        </Card>
    </SwiperSlide>
);

const AlbumCover = ({ title, description, images }: MultimediaT) => (
    // make something similar to an photo album cover
    <Card>
        <CardContent>
            <Typography variant="fancy_h3">{title}</Typography>
            {/* start date - end date from images */}
            {/* description? */}
        </CardContent>
    </Card>
)

const Multimedia = () => {
    return (
        <Stack>
            <Stack>
                <Typography variant="fancy_h1" textAlign="center"><HighlightedLetter letter="Memories"/></Typography>
                <Typography variant="subtitle1" textAlign="center">Description</Typography>
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
                        description: multimedia.description,
                        image: multimedia.images[getRandomIntBetween(multimedia.images.length)]
                    }
                }).map(PreviewCard)}
            </Swiper>
            <Divider/>
            <Typography variant="h2" textAlign="center">Wayback Machine</Typography>
            <Divider/>
            {fakeMultimediaData.map(AlbumCover)}
        </Stack>
    );
}


export default Multimedia

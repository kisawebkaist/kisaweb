import Lister from "../../components/lister";
import React, { useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button } from "@mui/material";
import "../../components/css/multimedia.css"

const fakeCarouselData = ["facebook-logo.png", "kisaLogo.png", "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"]
const fakeImageData = [""]
const styles = {
    card: {
        margin: '15px 10px',
        padding: 0,
        borderRadius: '16px',
        backgroundColor: 'lightskyblue'
    },
    small: {
        gridRowEnd: 'span 26'
    },
    medium: {
        gridRowEnd: 'span 33'
    },
    large: {
        gridRowEnd: 'span 45'
    }
}

const CardRender = ({ data }: { data: string }) => {
    const [hover, setHover] = useState(false);

    const cardStyle = {
        boxShadow: hover
            ? 'rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px'
            : '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
        transform: hover ? 'scale(1.05)' : 'scale(1)'
    };

    return (
        <Card className="card" style={cardStyle}
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <CardContent className="cardContent">
                <span className="date">date</span>
                <img src={data} />
                <span className="headline">HeadLine</span>
            </CardContent>
        </Card>
    );
}

const CarouselRender = ({ data }: { data: string[] }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    return (
        <div className="carouselContainer">
            <center>
                <span className="bgText">OUR PROUDLY PRESENT</span>
                <div className="carousel">
                    {data.map((image, index) => (
                        <CardRender data={image} />
                    ))}
                </div>
                <div>
                    <br />
                    <span className="dot" ></span>
                    <span className="dot" ></span>
                    <span className="dot" ></span>
                    <br />
                    <br />
                </div>
            </center>
        </div>
    );
}

type CardProps = {
    size: "small" | "medium" | "large";
};

function PinterestCard(props: CardProps) {
    return (
        <div style={{
            ...styles.card,
            ...styles[props.size]
        }}>
            <img src = "facebook-logo.png" width="10%" height="10%"/>
        </div>
    )
}

const PinterestRender = () => {
    return (
        <div className="pinterestContainer">
            <PinterestCard size = "small"/>
            <PinterestCard size = "medium"/>
            <PinterestCard size = "large"/>
            <PinterestCard size = "small"/>
        </div>
    )
}

const Multimedia = () => {
    return (
        <>
            <center>
                <h2>Multimedia</h2>
            </center>
            <br />
            <br />
            <div className="carousel">
                <CarouselRender data={fakeCarouselData} />
            </div>
            <br />
            <br />
            <div>
                <PinterestRender />
            </div>
        </>
    )
}



export default Multimedia
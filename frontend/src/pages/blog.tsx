import React, { useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Lister from "../components/lister"
import "../components/css/blog.css"

/**
 * @brief This can be used as a structure of blog data for api.
 */
export type BlogDataT = {
    date: string;
    headline: string;
    passageLink: string;
    tags: string[];
};

const BlogRender = ({ data }: { data: BlogDataT }) => {
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
                <span className="date">{data.date}</span>
                <span className="headline"><a href={data.passageLink}>{data.headline}</a></span>
                <span className="tag">{data.tags.join(', ')}</span>
            </CardContent>
        </Card>
    );
}

const fakeBlogData: BlogDataT[] = [
    {
        date: "25 Aug 2023",
        headline: "Lorem Ipsum",
        passageLink: "#",
        tags: ["#Lorem ipsum dolor sit amet"]
    },

    {
        date: "16 Feb 1971",
        headline: "TOP SECRET DON'T CLICK ME",
        passageLink: "https://www.youtube.com/watch?v=BbeeuzU5Qc8",
        tags: ["#kisaWebTeamIsDaBest", "#NeverGonnaGiveYouUp"]
    },

    {
        date: "1 Jan 2000",
        headline: "Funny clip of Jowi",
        passageLink: "https://www.youtube.com/shorts/KKlT6kReCZs",
        tags: ["#WeLoveOurHead"]
    }
]

const Blog = () => {
    return <>
        <center>
            <h1>Blog</h1>
        </center>

        <div className = "cardContainer">
        <Lister
            array={fakeBlogData}
            render={BlogRender}
            props={{}}
        />
        </div>
    </>
}

export default Blog
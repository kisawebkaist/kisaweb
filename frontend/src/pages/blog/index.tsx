import React, { useState, useEffect } from "react";
import BlogAPI from "../../API/blog";
import axios from 'axios';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button } from "@mui/material";
import Lister from "../../components/lister"
import "../../components/css/blog.css"

/**
 * @brief This can be used as a structure of blog data for api.
 */
export type BlogDataT = {
    date: string;
    headline: string;
    brief: string;
    passageLink: string;
    tags: string[];
};

const fakeBlogData: BlogDataT[] = [
    {
        date: "25 Aug 2023",
        headline: "Lorem Ipsum",
        brief: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
        passageLink: "#",
        tags: ["#Lorem ipsum dolor sit amet"]
    },

    {
        date: "16 Feb 1971",
        headline: "TOP SECRET DON'T CLICK ME",
        brief: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
        passageLink: "https://www.youtube.com/watch?v=BbeeuzU5Qc8",
        tags: ["#kisaWebTeamIsDaBest", "#NeverGonnaGiveYouUp"]
    },

    {
        date: "1 Jan 2000",
        headline: "Funny clip of Jowi",
        brief: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
        passageLink: "https://www.youtube.com/shorts/KKlT6kReCZs",
        tags: ["#WeLoveOurHead"]
    }
]

const ReadMoreButton = ({ link }: { link: string }) => {
    return (
        <div className="readMore">
            <a href={link} className="readMoreText">Read More &raquo;</a>
        </div>
    )
}

const CardRender = ({ data }: { data: BlogDataT }) => {
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
                <img src="https://media.makeameme.org/created/the-code-works-e47061d20f.jpg" />
                <span className="headline"><a href={data.passageLink}>{data.headline}</a></span>
                <span className="tag">{data.tags.join(', ')}</span>
            </CardContent>
        </Card>
    );
}

const ListRender = ({ data }: { data: BlogDataT }) => {
    return (
        <div className="listViewContainer">
            <img src="https://pleated-jeans.com/wp-content/uploads/2023/10/funniest-programming-memes-from-this-week-october-14-2023-1.png" />
            <div className="textData">
                <span className="tag">{data.tags.join(', ')}</span>
                <a href={data.passageLink}>{data.headline}</a>
                <span className="subtext">{data.brief}</span>
                <ReadMoreButton link={data.passageLink} />
            </div>
        </div>
    )
}

const filteredBlog = (category: string, blogData: BlogDataT[]): BlogDataT[] => {
    if (category === 'All') {
        return blogData;
    }

    return blogData.filter(blog => {
        return blog.tags.includes(category);
    });
};


const Blog = () => {
    const [selectedCategory, setSelectedCategory] = useState<string>('All');
    const [allUniqueTags, setAllUniqueTags] = useState<string[]>([]);

    const relatedBlog = filteredBlog(selectedCategory, fakeBlogData);
    useEffect(() => {
        const fetchTags = async () => {
          try {
            const tags = await BlogAPI.allTags({ someQueryParam: 'value' });
            setAllUniqueTags(tags.map(tag => tag.tag_name));
          } catch (error) {
            console.error('Error fetching tags:', error);
          }
    };
    
        fetchTags();
      }, []);
    return (
        <>
            <div className="featuredPost">
                <center>
                    <h1>Featured Content</h1>
                </center>
                <div className="cardContainer">
                    <Lister
                        array={fakeBlogData}
                        render={CardRender}
                        props={{}}
                    />
                </div>
            </div>

            <center>
                <h2>Categories</h2>
                <div className="buttonStyle">
                    {allUniqueTags.map((tag) => (
                        <Button
                            className={selectedCategory === tag ? 'activeButton' : ''}
                            onClick={() => setSelectedCategory(tag)}>
                            {tag}
                        </Button>
                    ))}
                </div>
            </center>
            <div>
                <Lister
                    array={relatedBlog}
                    render={ListRender}
                    props={{}}
                />
            </div>
        </>
    )
}

export default Blog

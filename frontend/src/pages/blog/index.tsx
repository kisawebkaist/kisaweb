import React, { useState } from "react";
import BlogAPI, { PartialBlogAPI, TagT } from "../../API/blog";
// import Card from "@mui/material/Card";
// import CardContent from "@mui/material/CardContent";
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Chip,
  Container,
  Divider,
  Grid,
  Icon,
  Link,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import Lister from "../../components/lister";
import "../../components/css/blog.css";
import QueryGuard from "../../components/query-guard";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faImage } from "@fortawesome/free-regular-svg-icons";
import { useNavigate } from "react-router-dom";
import { render } from "@testing-library/react";
import { arch } from "os";
import { HighlightedLetter } from "../../core/components";

// /**
//  * @brief This can be used as a structure of blog data for api.
//  */
// export type BlogDataT = {
//   date: string;
//   headline: string;
//   brief: string;
//   passageLink: string;
//   tags: string[];
// };

// const fakeBlogData: BlogDataT[] = [
//   {
//     date: "25 Aug 2023",
//     headline: "Lorem Ipsum",
//     brief:
//       "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
//     passageLink: "#",
//     tags: ["#Lorem ipsum dolor sit amet"],
//   },

//   {
//     date: "16 Feb 1971",
//     headline: "TOP SECRET DON'T CLICK ME",
//     brief:
//       "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
//     passageLink: "https://www.youtube.com/watch?v=BbeeuzU5Qc8",
//     tags: ["#kisaWebTeamIsDaBest", "#NeverGonnaGiveYouUp"],
//   },

//   {
//     date: "1 Jan 2000",
//     headline: "Funny clip of Jowi",
//     brief:
//       "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus justo diam, vitae fermentum orci condimentum in. Aliquam erat volutpat. Sed congue scelerisque mi, et ornare arcu fringilla id.",
//     passageLink: "https://www.youtube.com/shorts/KKlT6kReCZs",
//     tags: ["#WeLoveOurHead"],
//   },
// ];

// const ReadMoreButton = ({ link }: { link: string }) => {
//   return (
//     <div className="readMore">
//       <a href={link} className="readMoreText">
//         Read More &raquo;
//       </a>
//     </div>
//   );
// };

// const CardRender = ({ data }: { data: BlogDataT }) => {
//   const [hover, setHover] = useState(false);

//   const cardStyle = {
//     boxShadow: hover
//       ? "rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px"
//       : "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
//     transition: "transform 0.3s ease, box-shadow 0.3s ease",
//     transform: hover ? "scale(1.05)" : "scale(1)",
//   };

//   return (
//     <Card
//       className="card"
//       style={cardStyle}
//       onMouseEnter={() => setHover(true)}
//       onMouseLeave={() => setHover(false)}
//     >
//       <CardContent className="cardContent">
//         <span className="date">{data.date}</span>
//         <img src="https://media.makeameme.org/created/the-code-works-e47061d20f.jpg" />
//         <span className="headline">
//           <a href={data.passageLink}>{data.headline}</a>
//         </span>
//         <span className="tag">{data.tags.join(", ")}</span>
//       </CardContent>
//     </Card>
//   );
// };

function sortBlogsByDateModified(blogs: PartialBlogAPI[]) {
  return blogs.sort((a, b) => new Date(b.data.modified).getTime() - new Date(a.data.modified).getTime());
}

const BlogCard = ({ data: blog }: { data: PartialBlogAPI }) => {
  const navigate = useNavigate();
  const renderBlogTagChip = (tag_name: string) => (
    <Chip label={tag_name} />
  );

  return (
    <Grid item xs={12} sm={6} md={4} lg={3}>
      <Card>
        <CardActionArea onClick={() => navigate(`./${blog.data.slug}`)}>
          <CardMedia
            component="img"
            alt=""
            image="/kisaLogo.png"
          />
          <CardContent>
          <Stack rowGap={1}>
            <Typography variant="caption">
              {new Date(blog.data.modified).toDateString()}
            </Typography>
            <Typography
                variant="h2"
                fontSize="large"
                fontWeight="bold"
              >
                {blog.data.title}
              </Typography>
              <Typography fontStyle="italic">
              {blog.data.description}
            </Typography>
            <Stack direction="row" gap={1}>
              {blog.data.tags.map((tag=>tag.tag_name)).map(renderBlogTagChip)}
            </Stack>
          </Stack>
          </CardContent>
        </CardActionArea>
      </Card>
      {/* <Paper className="flex flex-col justify-center items-center gap-y-2 p-4">
        <Icon color="primary" className="w-40 h-40 opacity-50 ">
          <FontAwesomeIcon icon={faImage} className="text-9xl opacity-80" />
        </Icon>
        <Divider orientation="horizontal" flexItem/>
        <Stack direction="column" justifyContent="center" className="h-12">
        </Stack>
        
        <Button
          className="w-full justify-self-end"
          variant="contained"
          onClick={() => navigate(`./${blog.data.slug}`)}
        >
          Read
        </Button>
      </Paper> */}
    </Grid>
  );
  // return (
  //   <div className="listViewContainer">
  //     <img src="https://pleated-jeans.com/wp-content/uploads/2023/10/funniest-programming-memes-from-this-week-october-14-2023-1.png" />
  //     <div className="textData">
  //       <span className="tag">{data.tags.join(", ")}</span>
  //       <a href={data.passageLink}>{data.headline}</a>
  //       <span className="subtext">{data.brief}</span>
  //       <ReadMoreButton link={data.passageLink} />
  //     </div>
  //   </div>
  // );
};

// const filteredBlog = (
//   category: string,
//   blogData: PartialBlogAPI[]
// ): PartialBlogAPI[] => {
//   if (category === "All") {
//     return blogData;
//   }

//   return blogData.filter((blog) => {
//     return blog.tags.includes(category);
//   });
// };

type TagP = {
  data: string;
  id: number;
  onClick: (data: string) => void;
};
const Tag = ({ data: tagName, id, onClick }: TagP) => {
  return (
    <Button variant="outlined" onClick={() => onClick(tagName)}>
      {tagName}
    </Button>
  );
};

type BlogP = {
  blogs: PartialBlogAPI[];
  tags: TagT[];
};

const Blog = ({ blogs, tags }: BlogP) => {
  // const tagNames = React.useMemo(() => tags.map((tag) => tag.tag_name), [tags]);
  sortBlogsByDateModified(blogs);

  function renderLastestRelease(blogs: PartialBlogAPI[]) {
    const current = new Date();
    const lastMonth = new Date(current.getTime()-30*24*60*60*1000);
    const toRender = blogs.filter(blog => new Date(blog.data.modified) >= lastMonth);

    return ([
      <Typography variant="h2" color="main">Latest Release</Typography>,
      <Grid container spacing={4} className="p-4">
        <Lister array={toRender} render={BlogCard} props={undefined} />
      </Grid>,
      <Divider/>
    ]);
  }
  
  function renderBlogCards(blogs: PartialBlogAPI[]) {
    let yearArchives: JSX.Element[] = [];
    let currentYear = new Date(blogs[0].data.modified).getFullYear();
    let currentYearArchive: JSX.Element[] = [];

    function archiveCurrentYear() {
      if (currentYearArchive.length !== 0) {
        yearArchives.push(<Typography variant="h2">{currentYear}</Typography>);
        yearArchives.push(
          <Grid container spacing={4} className="p-4">
            {currentYearArchive}
          </Grid>
        );
        yearArchives.push(<Divider/>);
      }
    }

    if (blogs.length > 0) {
      for (let blog of blogs) {
        let year = new Date(blog.data.modified).getFullYear();
        if (year !== currentYear) {
          archiveCurrentYear();
          currentYear = year;
          currentYearArchive = [];
        } else {
          currentYearArchive.push(<BlogCard data={blog} />);
        }
      }
      archiveCurrentYear();
    }
    return yearArchives;
  }

  /*
    the idea about tag-filtering is good but there are some problems
    - tags are not categories, i.e. they are not mutually exclusive (so we might need some kind of checkbox list)
    - there can be a lot of tags, i mean "a lot" and how would we implement it for mobile?
  */
  return (
    <Stack>
      {/* <Stack direction="column" alignItems="center">
        <Typography variant="h4" className="my-4">
          Tags
        </Typography>
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="center"
          className="overflow-auto max-width-2/3 gap-x-4"
        >
          <Lister
            array={tagNames}
            props={{ onClick: setSelectedCategory }}
            render={Tag}
          />
        </Stack>
      </Stack> */}
      <Stack textAlign="center">
        <Typography variant="fancy_h1" textAlign="center"><HighlightedLetter letter="KISA" /> Blog</Typography>
        <Typography variant="subtitle1">Sharing is Caring</Typography>
      </Stack>
      {renderLastestRelease(blogs)}
      <Typography variant="h2" textAlign="center">All blogs</Typography>
      <Divider/>
      {renderBlogCards(blogs)}
    </Stack>
  );
};

const BlogGuard = () => {
  const blogAndCategoryQuery = React.useCallback(() => {
    return Promise.all([BlogAPI.allBlogs({}), BlogAPI.allTags({})]).then(
      ([blogs, tags]) => {
        return {
          blogs,
          tags,
        };
      }
    );
  }, []);
  return (
    <QueryGuard
      query={blogAndCategoryQuery}
      args={{}}
      render={Blog}
      props={{}}
    />
  );
};

export default BlogGuard;

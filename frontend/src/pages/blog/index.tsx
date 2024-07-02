import React, { useState } from "react";
import BlogAPI, { PartialBlogAPI, TagT } from "../../API/blog";
// import Card from "@mui/material/Card";
// import CardContent from "@mui/material/CardContent";
import {
  Button,
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

const BlogCard = ({ data: blog }: { data: PartialBlogAPI }) => {
  const navigate = useNavigate();
  return (
    <Grid item xs={3}>
      <Paper className="flex flex-col justify-center items-center gap-y-2 p-4">
        <Icon color="primary" className="w-40 h-40 opacity-50 ">
          <FontAwesomeIcon icon={faImage} className="text-9xl opacity-80" />
        </Icon>
        <Divider orientation="horizontal" flexItem/>
        <Stack direction="column" justifyContent="center" className="h-12">
          <Typography
            variant="h2"
            fontSize="large"
            className="text-center font-bold text-center"
          >
            {blog.data.title}
          </Typography>
        </Stack>
        <Typography variant="body1" className="text-center h-20">
          {blog.data.description}
        </Typography>
        <Button
          className="w-full justify-self-end"
          variant="contained"
          onClick={() => navigate(`./${blog.data.slug}`)}
        >
          Read
        </Button>
      </Paper>
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
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");

  const relatedBlog = React.useMemo(() => {
    if (selectedCategory === "ALL") return blogs;
    else
      return blogs.filter((blog) => blog.data.tags.includes(selectedCategory));
  }, [selectedCategory, blogs]);

  const tagNames = React.useMemo(() => tags.map((tag) => tag.tag_name), [tags]);
  return (
    <Stack>
      <Stack direction="column" alignItems="center">
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
      </Stack>
      <Grid container spacing={4} className="p-4">
        <Lister array={relatedBlog} render={BlogCard} props={{}} />
      </Grid>
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

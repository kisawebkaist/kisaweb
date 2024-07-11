import React from "react";
import { useParams } from "react-router-dom";
import QueryGuard from "../../../components/query-guard";
import BlogAPI, { CompleteBlogAPI } from "../../../API/blog";
import TextEditor from "@jowillianto/draftjs-wysiwyg/dist";
import { Box, Divider, Stack, Typography } from "@mui/material";

type BlogEntryP = {
  blog: CompleteBlogAPI;
};

const BlogEntry = ({ blog }: BlogEntryP) => {
  const content = React.useMemo(() => blog.get_content(), [blog]);
  return (
    <Stack direction="column" alignItems="center" className="gap-y-4 w-full">
      <Box className="py-10">
        <Typography variant="h1">
          {blog.data.title}
        </Typography>
        <Typography fontStyle="italic" textAlign="center">
          {blog.data.description}
        </Typography>
      </Box>
      <Divider
        orientation="horizontal"
        flexItem
        className="w-[98%] border-4 border-dashed rounded-xl"
      />
      <Box className = "px-32">
        <TextEditor
          defaultValue={content}
          editorBehaviour={{ readOnly: true }}
        />
      </Box>
    </Stack>
  );
};

const BlogEntryPage = () => {
  const params = useParams();
  const query = React.useCallback(() => {
    // This page will only be loaded when there is a slug argument
    const slug = params.slug as string;
    return BlogAPI.getBlog(slug).then((blog) => ({ blog }));
  }, [params]);
  return <QueryGuard render={BlogEntry} props={{}} args={{}} query={query} />;
};

export default BlogEntryPage;

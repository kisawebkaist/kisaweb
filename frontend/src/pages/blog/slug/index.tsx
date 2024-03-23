import React from "react";
import { useParams } from "react-router-dom";
import QueryGuard from "../../../components/query-guard";
import BlogAPI, { CompleteBlogAPI } from "../../../API/blog";
import TextEditor from '@jowillianto/draftjs-wysiwyg/dist'

type BlogEntryP = {
  blog : CompleteBlogAPI
}

const BlogEntry = ({blog} : BlogEntryP) => {
  const content = React.useMemo(() => blog.get_content(), [blog])
  return (
    <TextEditor
      defaultValue = {content}
    />
  )
}

const BlogEntryPage = () => {
  const params = useParams()
  const query = React.useCallback(() => {
    // This page will only be loaded when there is a slug argument
    const slug = params.slug as string
    return BlogAPI.getBlog(slug).then((blog) => ({ blog }))
  }, [ params ])
  return (
    <QueryGuard
      render = {BlogEntry}
      props = {{}}
      args = {{}}
      query = {query}
    />
  )
}

export default BlogEntryPage

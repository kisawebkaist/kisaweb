import axios from "axios";
import {
  convertFromHTML,
  ContentState,
  convertToRaw,
  RawDraftContentState,
} from "draft-js";

type BlogT_Complete = {
  title: string;
  description: string;
  content: string;
  new_content: RawDraftContentState;
  created: string;
  modified: string;
  slug: string;
  tags: string;
};
type BlogT_Partial = Omit<BlogT_Complete, "new_content" | "content">;
type TagT = { tag_name: string };

export class CompleteBlogAPI {
  data: BlogT_Complete;
  content?: RawDraftContentState;
  constructor(blog: BlogT_Complete) {
    this.data = blog;
    this.content = undefined;
  }
  get_content(): RawDraftContentState {
    if (this.content === undefined && this.data.content.length === 0) {
      this.content = this.data.new_content;
    } else if (this.content === undefined) {
      const blocks = convertFromHTML(this.data.content);
      const contentState = ContentState.createFromBlockArray(
        blocks.contentBlocks,
        blocks.entityMap
      );
      const rawState = convertToRaw(contentState);
      this.content = rawState;
      axios.post(
        `${process.env.REACT_APP_API_ENDPOINT}blog/${this.data.slug}`,
        { new_content: rawState }
      );
    }
    return this.content;
  }
}

export class PartialBlogAPI {
  data: BlogT_Partial;
  constructor(blog: BlogT_Partial) {
    this.data = blog;
  }
}

export default class BlogAPI {
  static allBlogs(queryParams: Record<string, any>): Promise<PartialBlogAPI[]> {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}blog/`, queryParams)
      .then((resp) =>
        resp.data.map((blog: BlogT_Partial) => new PartialBlogAPI(blog))
      );
  }
  static getBlog(slug: string) {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}blog/${slug}`)
      .then((resp) => new CompleteBlogAPI(resp.data));
  }
  static allTags(queryParams: Record<string, any>): Promise<TagT[]> {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}blog/tags`, queryParams)
      .then((resp) => resp.data);
  }
}

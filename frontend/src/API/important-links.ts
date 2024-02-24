import axios from "axios";
import { CategoryT } from "./faq";

type ImportantLinkCategoryT = {
  title_category: string;
  id: number;
};

type LinkT = {
  title: string;
  url: string;
  description: string;
  category: number;
  is_english: boolean;
  requires_sso: boolean;
  external_access: boolean;
};

export default class ImportantLinks {
  data: Omit<LinkT, "category"> & { category: ImportantLinkCategoryT };
  constructor(data: ImportantLinks["data"]) {
    this.data = data;
  }

  static links(): Promise<{
    links: ImportantLinks[];
    categories: ImportantLinkCategoryT[];
  }> {
    return Promise.all([
      axios.get(`${process.env.REACT_APP_API_ENDPOINT}important-links`),
      axios.get(
        `${process.env.REACT_APP_API_ENDPOINT}important-links/categories`
      ),
    ]).then(([linkResp, categoryResp]) => {
      const categoryHash = (
        categoryResp.data as ImportantLinkCategoryT[]
      ).reduce((prev, cur) => {
        prev[cur.id] = cur;
        return prev;
      }, {} as Record<number, ImportantLinkCategoryT>);
      const links = linkResp.data.map((link: LinkT) => ({
        ...link,
        category: categoryHash[link.category],
      }));
      return { links, categories : categoryResp.data}
    });
  }
}
